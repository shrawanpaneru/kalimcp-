import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_kali_mcp():
    # Define server parameters - adjust path to docker and image as needed
    # Note: Using absolute path to docker found earlier
    docker_path = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"
    server_params = StdioServerParameters(
        command=docker_path,
        args=["run", "-i", "--rm", "kali-mcp"],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            print("Listing tools...")
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            print("\nTesting 'scan_host' on localhost...")
            result = await session.call_tool("scan_host", {"target": "localhost", "options": "-F"})
            print(f"Scan Result:\n{result.content[0].text}")

if __name__ == "__main__":
    try:
        asyncio.run(test_kali_mcp())
    except Exception as e:
        print(f"Test failed: {e}")
