# Ona JetBrains Development Container
FROM mcr.microsoft.com/devcontainers/universal:2

# Install additional tools
RUN apt-get update && apt-get install -y \
    vim \
    curl \
    wget \
    jq \
    htop \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (optional - for local LLM)
# Note: Ollama installation can be done manually after container starts
# Run: curl -fsSL https://ollama.com/install.sh | sh
# This avoids security concerns with piping curl to shell during build

# Set up Python environment
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Set working directory
WORKDIR /workspaces

# Environment variables
ENV PYTHONPATH=/workspaces
ENV PYTHONDONTWRITEBYTECODE=1
ENV EDITOR=vim

# Healthcheck - verify Node.js and Python are functional
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "process.exit(0)" && python -c "import sys; sys.exit(0)" || exit 1

# Labels for JetBrains
LABEL maintainer="Scarmonit"
LABEL description="Ona JetBrains Development Environment"
LABEL ona.jetbrains.enabled="true"
