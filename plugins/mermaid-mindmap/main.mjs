// mermaid-mindmap — transform a nested outline into a Mermaid `mindmap`
// block. Pure JS, no network. Output is meant to be rendered by Ghast's
// Mermaid artifact renderer (or pasted into any Mermaid-aware tool).
//
// Inspired by lobe-chat-plugins' `moonlit-mind-map`, but doesn't depend
// on any remote service.

export function activate(context) {
  const handle = context.tools.register("build_mindmap", {
    description:
      "Convert a structured outline into a Mermaid `mindmap` code block. " +
      "Pass `root` for the central node and `branches` as an array of nodes; " +
      "each node has a `label` and an optional `children` array. Returns a " +
      "string starting with ```mermaid that the chat will render as a tree.",
    parameters: {
      type: "object",
      properties: {
        root: {
          type: "string",
          description: "Label of the central mindmap node.",
        },
        branches: {
          type: "array",
          description: "Top-level branches off the root.",
          items: {
            type: "object",
            properties: {
              label: { type: "string" },
              children: { type: "array" },
            },
            required: ["label"],
          },
        },
      },
      required: ["root", "branches"],
    },
    execute: async (args = {}) => {
      const { root, branches } = args ?? {};
      if (typeof root !== "string" || !root.trim()) {
        throw new Error("`root` must be a non-empty string.");
      }
      if (!Array.isArray(branches)) {
        throw new Error("`branches` must be an array.");
      }

      const escape = (text) =>
        String(text).replace(/[\r\n]+/g, " ").replace(/[\(\)]/g, " ").trim();

      const renderNode = (node, depth) => {
        const indent = "  ".repeat(depth);
        const lines = [`${indent}${escape(node.label)}`];
        if (Array.isArray(node.children)) {
          for (const child of node.children) {
            lines.push(renderNode(child, depth + 1));
          }
        }
        return lines.join("\n");
      };

      const body = [
        `  root((${escape(root)}))`,
        ...branches.map((branch) => renderNode(branch, 2)),
      ].join("\n");

      const code = `\`\`\`mermaid\nmindmap\n${body}\n\`\`\``;
      return {
        code,
        nodeCount: countNodes(branches) + 1,
      };
    },
  });

  return { dispose: () => handle.dispose() };
}

function countNodes(branches) {
  let count = 0;
  for (const branch of branches ?? []) {
    count += 1;
    if (Array.isArray(branch.children)) {
      count += countNodes(branch.children);
    }
  }
  return count;
}
