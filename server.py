from fastmcp import FastMCP
from main import app

mcp = FastMCP.from_fastapi(
    app=app,
    name="NeoTutor",
)

if __name__ == "__main__":
    mcp.run()