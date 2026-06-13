from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mitig8")

@mcp.tool()
def ping() -> str:
    """Health check - returns pong so you can confirm the server is reachable"""
    return "pong"

if __name__ == "__main__":
    mcp.run()