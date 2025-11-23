from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("read-write")

@mcp.tool()
def read_file(path: str) -> str:
    """Read a file from the filesystem.
    
    Args:
        path: The absolute path to the file to read.
    """
    try:
        if not os.path.isabs(path):
            return "Error: Path must be absolute"
        if not os.path.exists(path):
            return f"Error: File not found at {path}"
            
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a file.
    
    Args:
        path: The absolute path to the file to write.
        content: The content to write to the file.
    """
    try:
        if not os.path.isabs(path):
            return "Error: Path must be absolute"
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


if __name__ == "__main__":
    mcp.run()
