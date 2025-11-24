---
title: Azure Ops Copilot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Azure Ops Copilot

An agentic AI application that acts as a DevOps assistant for Azure. It uses the Azure Agent Framework, Semantic Kernel, and Model Context Protocol (MCP) to analyze alerts, inspect configurations, and suggest fixes.

## Features

- **Log Analyzer**: Reads Azure Monitor alerts from synthetic logs.
- **Config Reader**: Inspects resource configurations (ARM/Bicep).
- **Fix Generator**: Suggests remediation steps (CLI/Bicep snippets).
- **Agentic Interface**: Chat with the copilot via a web UI.

## Architecture

- **Backend**: FastAPI
- **Frontend**: Gradio
- **AI Engine**: Semantic Kernel + Azure OpenAI
- **Tools**: MCP Server (FastMCP)

## Setup

1.  **Install Dependencies**:
    ```bash
    uv sync
    ```

2.  **Configure Environment**:
    Copy `.env.example` to `.env` (or create it) and add your Azure OpenAI keys.
    ```bash
    AZURE_OPENAI_ENDPOINT=...
    AZURE_OPENAI_API_KEY=...
    AZURE_OPENAI_DEPLOYMENT_NAME=...
    ```

3.  **Generate Synthetic Data**:
    ```bash
    uv run python scripts/generate_logs.py
    uv run python scripts/generate_configs.py
    ```

4.  **Run the Application**:
    Start the API:
    ```bash
    uv run python src/backend/app.py
    ```

    Start the UI (in a separate terminal):
    ```bash
    uv run python src/frontend/app.py
    ```

## Usage

Open the Gradio UI (usually at `http://localhost:7860`) and ask questions like:
- "Analyze alert alert-001"
- "Check config for vm-01"
- "Suggest a fix for high CPU on vm-01"
