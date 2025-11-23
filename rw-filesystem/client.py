import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    # Get absolute path to server.py
    server_path = os.path.abspath("server.py")
    
    # Use the current python interpreter
    python_exe = sys.executable
    
    print(f"Connecting to server at {server_path} using {python_exe}")
    
    server_params = StdioServerParameters(
        command=python_exe,
        args=[server_path],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools to verify
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Test file path
            test_file = os.path.abspath("test_mcp.txt")
            
            # Call write_file
            print(f"Writing to {test_file}...")
            result = await session.call_tool("write_file", arguments={"path": test_file, "content": "Hello from MCP Client!"})
            print(f"Write result: {result.content}")
            
            # Call read_file
            print(f"Reading from {test_file}...")
            content = await session.call_tool("read_file", arguments={"path": test_file})
            print(f"Read content: {content.content}")


if __name__ == "__main__":
    asyncio.run(run())
