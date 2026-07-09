from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "acme": {
            "transport": "http",
            "url": "http://mcp:8000/mcp",
        }
    }
)


async def get_mcp_tools():
    return await client.get_tools()