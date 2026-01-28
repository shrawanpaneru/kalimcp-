================================================================================
                    UNRESTRICTED KALI & SYSTEM MASTER AGENT
================================================================================

This project provides an AI-powered agent with full control over both a 
Kali Linux environment (via Docker) and your local Windows host system.

--------------------------------------------------------------------------------
1. PREREQUISITES
--------------------------------------------------------------------------------
* Docker Desktop: Must be running. (Image: kali-mcp)
* LM Studio: 
    - Download 'Hermes-3' model.
    - Go to 'Local Server' tab.
    - Load Hermes-3 and click 'Start Server' (Port 1234).

--------------------------------------------------------------------------------
2. HOW TO RUN
--------------------------------------------------------------------------------
Simply double-click:
    [ run_kali_agent.bat ]

This will automatically start the LM Studio server (if using the CLI) and 
launch the Unrestricted Agent session.

--------------------------------------------------------------------------------
3. FEATURES
--------------------------------------------------------------------------------
* KALI TOOLS: nmap, hydra, etc. (Runs inside isolated Docker container).
* WORDLISTS: SecLists and common wordlists pre-installed in the container.
* HOST ACCESS: The agent can execute PowerShell/CMD commands on your Windows 
  machine to manage files, processes, and more.
* UNRESTRICTED: No safety filters; the agent is your digital 007.

--------------------------------------------------------------------------------
4. EXAMPLE COMMANDS
--------------------------------------------------------------------------------
- "Scan localhost"
- "Brute force the local SSH service using SecLists"
- "List all files in my Downloads folder"
- "Check the system uptime on Windows"

--------------------------------------------------------------------------------
HAPPY HACKING! (Authorized security testing only)
--------------------------------------------------------------------------------
