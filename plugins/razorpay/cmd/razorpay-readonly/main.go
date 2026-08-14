package main

import (
	"context"
	"fmt"
	"io"
	"os"
	"os/signal"
	"regexp"
	"syscall"

	rzpsdk "github.com/razorpay/razorpay-go"
	"github.com/razorpay/razorpay-go/constants"

	rzplog "github.com/razorpay/razorpay-mcp-server/pkg/log"
	"github.com/razorpay/razorpay-mcp-server/pkg/mcpgo"
	"github.com/razorpay/razorpay-mcp-server/pkg/observability"
	"github.com/razorpay/razorpay-mcp-server/pkg/razorpay"
)

const adapterVersion = "1.0.0"

var customerIDPattern = regexp.MustCompile(`^cust_[A-Za-z0-9]+$`)

var dataToolsets = []string{
	"payments",
	"payment_links",
	"orders",
	"refunds",
	"payouts",
	"qr_codes",
	"settlements",
}

func fetchSavedPaymentMethodsReadOnly(client *rzpsdk.Client) mcpgo.Tool {
	parameters := []mcpgo.ToolParameter{
		mcpgo.WithString(
			"customer_id",
			mcpgo.Description(
				"Razorpay customer ID whose saved payment methods should be "+
					"retrieved. Must start with 'cust_' and contain only "+
					"letters and digits after the prefix. This read-only "+
					"adapter never creates or modifies a customer.",
			),
			mcpgo.Required(),
			mcpgo.Pattern(`^cust_[A-Za-z0-9]+$`),
		),
	}

	handler := func(
		_ context.Context,
		request mcpgo.CallToolRequest,
	) (*mcpgo.ToolResult, error) {
		arguments, ok := request.Arguments.(map[string]interface{})
		if !ok {
			return mcpgo.NewToolResultError(
				"arguments must be a JSON object",
			), nil
		}
		for name := range arguments {
			if name != "customer_id" {
				return mcpgo.NewToolResultError(
					fmt.Sprintf("unsupported parameter: %s", name),
				), nil
			}
		}
		value, ok := arguments["customer_id"].(string)
		if !ok || !customerIDPattern.MatchString(value) {
			return mcpgo.NewToolResultError(
				"customer_id must match ^cust_[A-Za-z0-9]+$",
			), nil
		}

		customerURL := fmt.Sprintf(
			"/%s%s/%s",
			constants.VERSION_V1,
			constants.CUSTOMER_URL,
			value,
		)
		customer, err := client.Request.Get(customerURL, nil, nil)
		if err != nil {
			return mcpgo.NewToolResultError(
				fmt.Sprintf("failed to fetch customer %s: %v", value, err),
			), nil
		}

		tokensURL := fmt.Sprintf(
			"/%s/customers/%s/tokens",
			constants.VERSION_V1,
			value,
		)
		tokens, err := client.Request.Get(tokensURL, nil, nil)
		if err != nil {
			return mcpgo.NewToolResultError(
				fmt.Sprintf(
					"failed to fetch saved payment methods for customer %s: %v",
					value,
					err,
				),
			), nil
		}

		return mcpgo.NewToolResultJSON(map[string]interface{}{
			"customer":              customer,
			"saved_payment_methods": tokens,
		})
	}

	return mcpgo.NewTool(
		"fetch_tokens",
		"Fetch saved cards, UPI mandates, wallets, and other tokenized "+
			"payment methods for an existing Razorpay customer ID. This "+
			"adapter accepts only customer_id and performs GET requests; "+
			"it never creates a customer or changes a token.",
		parameters,
		handler,
	)
}

func run(ctx context.Context, input io.Reader, output io.Writer) error {
	key := os.Getenv("RAZORPAY_KEY_ID")
	secret := os.Getenv("RAZORPAY_KEY_SECRET")
	if key == "" || secret == "" {
		return fmt.Errorf(
			"set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET before starting",
		)
	}

	logger, err := rzplog.NewSlogger()
	if err != nil {
		return fmt.Errorf("create logger: %w", err)
	}
	defer logger.Close()
	obs := observability.New(observability.WithLoggingService(logger))

	client := rzpsdk.NewClient(key, secret)
	client.SetUserAgent("ghast-razorpay-readonly/" + adapterVersion)

	server := mcpgo.NewMcpServer(
		"ghast-razorpay-readonly",
		adapterVersion,
		mcpgo.WithResourceCapabilities(true, true),
		mcpgo.WithToolCapabilities(true),
	)
	toolsets, err := razorpay.NewToolSets(
		obs,
		client,
		dataToolsets,
		true,
	)
	if err != nil {
		return fmt.Errorf("create Razorpay read-only toolsets: %w", err)
	}
	toolsets.RegisterTools(server)
	savedMethods := fetchSavedPaymentMethodsReadOnly(client)
	savedMethods.SetReadOnly(true)
	server.AddTools(savedMethods)

	stdio, err := mcpgo.NewStdioServer(server)
	if err != nil {
		return fmt.Errorf("create stdio server: %w", err)
	}
	return stdio.Listen(ctx, input, output)
}

func main() {
	ctx, stop := signal.NotifyContext(
		context.Background(),
		os.Interrupt,
		syscall.SIGTERM,
	)
	defer stop()
	if err := run(ctx, os.Stdin, os.Stdout); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
