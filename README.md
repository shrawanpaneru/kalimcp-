================================================================================
                    UNRESTRICTED KALI & SYSTEM MASTER AGENT
================================================================================

This project provides an AI-powered agent with full control over both a 
Kali Linux environment (via Docker) and your local Windows host system.

--------------------------------------------------------------------------------
1. MINIMUM REQUIREMENTS
--------------------------------------------------------------------------------
* DISK SPACE: At least 60 GB free (Kali + Models + Tools).
* RAM: 16 GB Recommended (to run Docker + LM Studio + Python Agent).
* GPU: NVIDIA/AMD GPU recommended for LM Studio (but CPU works).
* OS: Windows 10/11 with Docker Desktop installed.

--------------------------------------------------------------------------------
1. INSTALLATION (How to set up from scratch)
--------------------------------------------------------------------------------
1. INSTALL DOCKER:
   - Download and install Docker Desktop for Windows.
   - Ensure it is RUNNING before starting the agent.

2. INSTALL LM STUDIO:
   - Run: `winget install ElementLabs.LMStudio` in your terminal.
   - Open the app, search for "Hermes-3", and download it.

3. SET UP PROJECT:
   - Open a terminal in this folder.
   - Build the Kali image: 
     & "C:\Program Files\Docker\Docker\resources\bin\docker.exe" build -t kali-mcp .
   - Install Python dependencies:
     pip install mcp httpx ollama

4. PULL OLLAMA MODELS (Optional fallback):
   - Run: `ollama pull hermes3`

--------------------------------------------------------------------------------
2. PREREQUISITES
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

