package main

import (
	"context"
	"encoding/json"
	"fmt"
	"testing"

	rzpsdk "github.com/razorpay/razorpay-go"
	"github.com/razorpay/razorpay-go/constants"

	"github.com/razorpay/razorpay-mcp-server/pkg/mcpgo"
	"github.com/razorpay/razorpay-mcp-server/pkg/razorpay/mock"
)

func TestFetchSavedPaymentMethodsReadOnly(t *testing.T) {
	customerID := "cust_1Aa00000000003"
	customer := map[string]interface{}{
		"id":      customerID,
		"entity":  "customer",
		"contact": "9876543210",
	}
	tokens := map[string]interface{}{
		"entity": "collection",
		"count":  float64(1),
		"items": []interface{}{
			map[string]interface{}{
				"id":     "token_ABCDEFGH",
				"method": "card",
			},
		},
	}
	httpClient, server := mock.NewHTTPClient(
		mock.Endpoint{
			Path: fmt.Sprintf(
				"/%s%s/%s",
				constants.VERSION_V1,
				constants.CUSTOMER_URL,
				customerID,
			),
			Method:   "GET",
			Response: customer,
		},
		mock.Endpoint{
			Path: fmt.Sprintf(
				"/%s/customers/%s/tokens",
				constants.VERSION_V1,
				customerID,
			),
			Method:   "GET",
			Response: tokens,
		},
	)
	defer server.Close()

	client := rzpsdk.NewClient("sample_key", "sample_secret")
	client.Request.BaseURL = server.URL
	client.Request.HTTPClient = httpClient
	tool := fetchSavedPaymentMethodsReadOnly(client)

	result, err := tool.GetHandler()(
		context.Background(),
		mcpgo.CallToolRequest{
			Arguments: map[string]interface{}{"customer_id": customerID},
		},
	)
	if err != nil {
		t.Fatal(err)
	}
	if result.IsError {
		t.Fatalf("unexpected tool error: %s", result.Text)
	}
	var actual map[string]interface{}
	if err := json.Unmarshal([]byte(result.Text), &actual); err != nil {
		t.Fatal(err)
	}
	if actual["customer"].(map[string]interface{})["id"] != customerID {
		t.Fatalf("unexpected customer: %#v", actual["customer"])
	}
	if actual["saved_payment_methods"].(map[string]interface{})["count"] !=
		float64(1) {
		t.Fatalf("unexpected tokens: %#v", actual["saved_payment_methods"])
	}
}

func TestFetchSavedPaymentMethodsReadOnlyRejectsMutationPath(t *testing.T) {
	client := rzpsdk.NewClient("sample_key", "sample_secret")
	tool := fetchSavedPaymentMethodsReadOnly(client)
	tests := []map[string]interface{}{
		{"contact": "9876543210"},
		{
			"customer_id": "cust_1Aa00000000003",
			"contact":     "9876543210",
		},
		{"customer_id": "invalid"},
		{},
	}
	for _, arguments := range tests {
		result, err := tool.GetHandler()(
			context.Background(),
			mcpgo.CallToolRequest{Arguments: arguments},
		)
		if err != nil {
			t.Fatal(err)
		}
		if !result.IsError {
			t.Fatalf("expected rejection for %#v", arguments)
		}
	}
}
