FROM kalilinux/kali-rolling

# Update and install basic tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    hydra \
    curl \
    git \
    wordlists \
    seclists \
    && apt-get clean

# Set working directory
WORKDIR /app

# Create a virtual environment for Python
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install MCP SDK
RUN pip3 install mcp

# Copy server code (will be created in next steps)
COPY server.py .

# Keep the container running or run the server
CMD ["python3", "server.py"]
