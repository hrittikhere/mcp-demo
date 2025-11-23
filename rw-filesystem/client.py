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
            
            # Test get_special_folder
            print("Testing get_special_folder...")
            home_path = await session.call_tool("get_special_folder", arguments={"folder": "home"})
            print(f"Home path: {home_path.content[0].text}")
            
            desktop_path = await session.call_tool("get_special_folder", arguments={"folder": "desktop"})
            print(f"Desktop path: {desktop_path.content[0].text}")

            # Test resolve_path
            print("Testing resolve_path...")
            rel_path = "test_mcp.txt"
            resolved_path = await session.call_tool("resolve_path", arguments={"path": rel_path})
            print(f"Resolved '{rel_path}' to: {resolved_path.content[0].text}")
            
            tilde_path = "~/Documents"
            resolved_tilde = await session.call_tool("resolve_path", arguments={"path": tilde_path})
            print(f"Resolved '{tilde_path}' to: {resolved_tilde.content[0].text}")

            # Use resolved path for file operations
            test_file = resolved_path.content[0].text
            
            # Call write_file
            print(f"Writing to {test_file}...")
            result = await session.call_tool("write_file", arguments={"path": test_file, "content": "Hello from MCP Client! Verified path resolution."})
            print(f"Write result: {result.content}")
            
            # Call read_file
            print(f"Reading from {test_file}...")
            content = await session.call_tool("read_file", arguments={"path": test_file})
            print(f"Read content: {content.content}")

            # Call list_directory
            current_dir = os.getcwd()
            print(f"Listing directory {current_dir}...")
            dir_content = await session.call_tool("list_directory", arguments={"path": current_dir})
            print(f"Directory content:\n{dir_content.content[0].text}")

            # Call search_files
            print(f"Searching for *.py files in {current_dir}...")
            search_content = await session.call_tool("search_files", arguments={"path": current_dir, "pattern": "*.py"})
            print(f"Search results:\n{search_content.content[0].text}")


if __name__ == "__main__":
    asyncio.run(run())
