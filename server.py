import asyncio
import subprocess
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server.stdio import stdio_server

server = Server("kali-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available Kali tools."""
    return [
        types.Tool(
            name="scan_host",
            description="Scan a host using nmap. Recommended for localhost testing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "The target to scan (e.g., localhost, 127.0.0.1)"},
                    "options": {"type": "string", "description": "Additional nmap options (e.g., -sV, -p-)"}
                },
                "required": ["target"]
            },
        ),
        types.Tool(
            name="brute_force",
            description="Attempt a brute-force attack using hydra on a service.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Target IP or hostname"},
                    "service": {"type": "string", "description": "Service to attack (e.g., ssh, http-get)"},
                    "user": {"type": "string", "description": "Username to test"},
                    "passlist": {"type": "string", "description": "Path to password list (or single password)"}
                },
                "required": ["target", "service", "user", "passlist"]
            },
        ),
        types.Tool(
            name="run_kali_tool",
            description="Run any Kali tool command directly. WARNING: Use with caution.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The full command to run (e.g., 'whoami', 'ls /')"}
                },
                "required": ["command"]
            },
        )
    ]

async def run_cmd_process(cmd: list[str]) -> str:
    """Helper to run a shell command and capture output."""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        output = stdout.decode().strip()
        error = stderr.decode().strip()
        
        if error:
            return f"Output:\n{output}\n\nErrors:\n{error}"
        return output if output else "Command executed successfully with no output."
    except Exception as e:
        return f"Error executing command: {str(e)}"

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if not arguments:
        return [types.TextContent(type="text", text="Error: No arguments provided.")]

    if name == "scan_host":
        target = arguments.get("target")
        options = arguments.get("options", "-F") # Default to fast scan
        cmd = ["nmap"] + options.split() + [target]
        result = await run_cmd_process(cmd)
        return [types.TextContent(type="text", text=result)]

    elif name == "brute_force":
        target = arguments.get("target")
        service = arguments.get("service")
        user = arguments.get("user")
        passlist = arguments.get("passlist")
        # Added -V for verbose output to show progress as requested
        cmd = ["hydra", "-V", "-l", user, "-p", passlist, target, service]
        result = await run_cmd_process(cmd)
        return [types.TextContent(type="text", text=result)]

    elif name == "run_kali_tool":
        command = arguments.get("command", "")
        # Very basic splitting for security/utility; in real scenarios, use with caution
        cmd = command.split()
        result = await run_cmd_process(cmd)
        return [types.TextContent(type="text", text=result)]

    return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kali-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
