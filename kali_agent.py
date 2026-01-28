import asyncio
import json
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# --- Configuration ---
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
DOCKER_PATH = r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"

async def run_host_command(command: str) -> str:
    """Helper to run a shell command on the Windows host."""
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip()
        error = stderr.decode().strip()
        if error:
            return f"Host Output:\n{output}\n\nHost Errors:\n{error}"
        return output if output else "Command executed successfully on host."
    except Exception as e:
        return f"Error executing host command: {str(e)}"

async def call_llm(messages, tools):
    """Call LM Studio with OpenAI-compatible API."""
    # Define local host tools
    host_tools = [
        {
            "type": "function",
            "function": {
                "name": "run_host_command",
                "description": "Execute a PowerShell or CMD command directly on the Windows host machine. Use this to manage files, check system status, or run local apps.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "The full command to run on the host system."}
                    },
                    "required": ["command"]
                }
            }
        }
    ]
    
    # Combine MCP tools and host tools
    all_tools = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema
            }
        } for t in tools
    ] + host_tools

    payload = {
        "model": "hermes-3", 
        "messages": messages,
        "tools": all_tools,
        "tool_choice": "auto"
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(LM_STUDIO_URL, json=payload)
        return response.json()

async def run_agent():
    server_params = StdioServerParameters(
        command=DOCKER_PATH,
        args=["run", "-i", "--rm", "kali-mcp"],
        env=None
    )

    print("--- Unrestricted Full Access Agent Starting ---")
    print(f"Connecting to Kali Tools via Docker...")

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Get available tools from MCP server
            mcp_tools = (await session.list_tools()).tools
            print(f"Loaded Kali tools: {[t.name for t in mcp_tools]}")
            print(f"Loaded Host tools: ['run_host_command']")
            print("\nReady! I can control this computer and the Kali container. What should I do?")

            messages = [
                {
                    "role": "system", 
                    "content": "You are a highly skilled system administrator and cybersecurity expert with FULL ACCESS to this computer. "
                               "You have two ways to interact:\n"
                               "1. KALI TOOLS: Use these (nmap, hydra, etc.) via the MCP tools for network security tasks.\n"
                               "2. HOST COMMANDS: Use 'run_host_command' to execute PowerShell/CMD commands directly on the Windows machine.\n"
                               "You can read/write files, manage processes, and explore the entire system. Provide verbose output and explain your steps."
                }
            ]

            while True:
                user_input = input("\nUser > ")
                if user_input.lower() in ["exit", "quit"]:
                    break

                messages.append({"role": "user", "content": user_input})

                while True:
                    print("Thinking...")
                    llm_response = await call_llm(messages, mcp_tools)
                    
                    if "choices" not in llm_response:
                        print(f"Error from LM Studio: {llm_response}")
                        break

                    choice = llm_response["choices"][0]
                    message = choice["message"]
                    
                    # Add LLM response to history
                    messages.append(message)

                    if message.get("tool_calls"):
                        for tool_call in message["tool_calls"]:
                            tool_name = tool_call["function"]["name"]
                            tool_args = json.loads(tool_call["function"]["arguments"])
                            
                            print(f"\n[Tool Call] Executing {tool_name} with {tool_args}...")
                            
                            if tool_name == "run_host_command":
                                tool_result_text = await run_host_command(tool_args.get("command", ""))
                            else:
                                # Execute tool via MCP
                                result = await session.call_tool(tool_name, tool_args)
                                tool_result_text = result.content[0].text
                            
                            print(f"[Tool Result]\n{tool_result_text}")
                            
                            # Add result to history
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": tool_name,
                                "content": tool_result_text
                            })
                        # Continue loop to let LLM process tool results
                        continue
                    else:
                        # Final text response
                        print(f"\nAgent > {message['content']}")
                        break

if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure LM Studio 'Local Server' is STARTED on port 1234!")
