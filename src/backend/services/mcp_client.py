from fastmcp import Client


class MCPClient:
    def __init__(self):
        self.mcp_path = "src/mcp/main.py"
        self.client = Client(self.mcp_path)

    def execute(self, tool_name, **kwargs):
        return self.client.call_tool(tool_name, **kwargs)
