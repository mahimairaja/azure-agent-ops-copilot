from fastmcp import Client


class MCPClient:
    def __init__(self):
        self.mcp_path = "src/mcp/main.py"
        self._client = None

    async def _get_client(self):
        """Get or create the MCP client."""
        if self._client is None:
            self._client = Client(self.mcp_path)
        return self._client

    async def execute(self, tool_name: str, **kwargs):
        """Execute a tool via the MCP client."""
        client = await self._get_client()
        async with client:
            result = await client.call_tool(tool_name, arguments=kwargs)
            # Extract the text content from the result
            if hasattr(result, "content") and result.content:
                return "\n".join(
                    item.text for item in result.content if hasattr(item, "text")
                )
            return str(result)

    async def list_tools(self):
        """List all available tools."""
        client = await self._get_client()
        async with client:
            return await client.list_tools()
