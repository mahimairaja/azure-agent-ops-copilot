import json
import os
from pathlib import Path

import gradio as gr
import pandas as pd
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def chat(message, history):
    """Send message to backend and get response."""
    try:
        response = requests.post(f"{API_URL}/chat", json={"message": message})
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"❌ Error: {str(e)}"


def load_alerts_data():
    """Load alerts data from JSON file."""
    try:
        alerts_file = DATA_DIR / "logs.json"
        if alerts_file.exists():
            with open(alerts_file, "r") as f:
                alerts = json.load(f)
            # Convert to DataFrame for better display
            df = pd.DataFrame(alerts)
            # Reorder columns for better readability
            columns = [
                "id",
                "severity",
                "description",
                "resource_id",
                "status",
                "created_at",
            ]
            df = df[columns]
            return df
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


def load_configs_data():
    """Load resource configs data from JSON file."""
    try:
        configs_file = DATA_DIR / "configs.json"
        if configs_file.exists():
            with open(configs_file, "r") as f:
                configs = json.load(f)
            # Flatten the data for better display
            flattened = []
            for config in configs:
                flat = {
                    "resource_id": config["resource_id"],
                    "type": config["type"],
                    "location": config["location"],
                    "compliance_status": config["compliance_status"],
                }
                flattened.append(flat)
            return pd.DataFrame(flattened)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


# Custom CSS for beautiful styling
custom_css = """
.gradio-container {
    font-family: 'Inter', sans-serif;
}

.header-container {
    text-align: center;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
}

.header-container h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.header-container p {
    font-size: 1.1rem;
    opacity: 0.95;
}

.info-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #667eea;
}

.tab-nav button {
    font-weight: 600;
    font-size: 1rem;
}

footer {
    text-align: center;
    padding: 1rem;
    color: #666;
    font-size: 0.9rem;
}
"""

# Create the Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
        neutral_hue="slate",
    ),
    css=custom_css,
    title="Azure Ops Copilot",
) as demo:
    # Header
    with gr.Row():
        gr.HTML(
            """
            <div class="header-container">
                <h1>🤖 Azure Ops Copilot</h1>
                <p>Your intelligent AI assistant for Azure Operations Management</p>
                <p style="font-size: 0.9rem; margin-top: 0.5rem;">
                    Powered by GPT-4o-mini • FastMCP • Semantic Kernel • Gradio UI • FastAPI
                </p>
                <div style="margin-top: 1.5rem;">
                    <a href="https://linkedin.com/in/mahimairaja" target="_blank" style="text-decoration: none;">
                        <button style="
                            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                            color: white;
                            border: none;
                            padding: 12px 32px;
                            font-size: 1.1rem;
                            font-weight: 700;
                            border-radius: 8px;
                            cursor: pointer;
                            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
                            transition: all 0.3s ease;
                            text-transform: uppercase;
                            letter-spacing: 1px;
                        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(255, 107, 107, 0.6)';"
                           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(255, 107, 107, 0.4)';">
                            🚀 Build Your Agent
                        </button>
                    </a>
                </div>
                <p style="font-size: 0.85rem; margin-top: 0.8rem; opacity: 0.9;">
                    Need a custom AI agent for your business? Let's build it together!
                </p>
            </div>
            """
        )

    # Tabs for different sections
    with gr.Tabs() as tabs:
        # Chat Tab
        with gr.Tab("💬 Chat Assistant", id=0):
            gr.Markdown(
                """
                ### Ask me anything about your Azure resources!

                I can help you:
                - 🔍 **Analyze alerts** - Get detailed analysis and root cause
                - ⚙️ **Check configurations** - View resource settings
                - 🔧 **Generate fixes** - Get Bicep templates and CLI commands
                """
            )

            chatbot = gr.ChatInterface(
                fn=chat,
                examples=[
                    "Analyze alert alert-001",
                    "Check config for vm-01",
                    "Suggest a fix for high CPU on vm-01",
                    "What alerts do we have?",
                ],
                type="messages",  # type: ignore
                chatbot=gr.Chatbot(
                    height=500,
                    show_copy_button=True,  # type: ignore
                    avatar_images=(
                        None,
                        "https://em-content.zobj.net/source/twitter/376/robot_1f916.png",
                    ),
                ),
            )

        # Sample Data Tab - Alerts
        with gr.Tab("📊 Sample Data: Alerts", id=1):
            gr.Markdown(
                """
                ### 🚨 Azure Monitor Alerts

                This is the sample alert data used by the copilot. You can reference these alert IDs in your queries.
                """
            )

            alerts_df = load_alerts_data()
            gr.Dataframe(
                value=alerts_df,
                interactive=False,
                wrap=True,
                column_widths=["10%", "10%", "30%", "35%", "8%", "15%"],
            )

            gr.Markdown(
                """
                **💡 Try asking:**
                - "Analyze alert alert-001"
                - "Show me critical alerts"
                - "What's the status of alert-005?"
                """
            )

        # Sample Data Tab - Configs
        with gr.Tab("⚙️ Sample Data: Resource Configs", id=2):
            gr.Markdown(
                """
                ### 🖥️ Azure Resource Configurations

                This is the sample resource configuration data. You can query these resources by their short names (e.g., "vm-01").
                """
            )

            configs_df = load_configs_data()
            gr.Dataframe(
                value=configs_df,
                interactive=False,
                wrap=True,
                column_widths=["50%", "25%", "12%", "13%"],
            )

            gr.Markdown(
                """
                **💡 Try asking:**
                - "Check config for vm-01"
                - "Show me the SQL database configuration"
                - "What's the compliance status of app-01?"
                """
            )

        # About Tab
        with gr.Tab("ℹ️ About", id=3):
            gr.Markdown(
                """
                ## About Azure Ops Copilot

                This is an intelligent AI-powered assistant designed to help you manage Azure operations more efficiently.

                ### 🎯 Features

                - **Alert Analysis**: Get instant analysis of Azure Monitor alerts with root cause identification
                - **Configuration Review**: Check resource configurations and compliance status
                - **Fix Generation**: Automatically generate Bicep templates and Azure CLI commands
                - **Natural Language Interface**: Just ask in plain English!

                ### 🛠️ Technology Stack

                - **Frontend**: Gradio
                - **Backend**: FastAPI
                - **AI Model**: GPT-4o-mini (Azure OpenAI)
                - **Agent Framework**: Semantic Kernel
                - **MCP Server**: FastMCP

                ### 📚 Sample Data

                The copilot uses synthetic sample data for demonstration purposes:
                - **10 sample alerts** across different Azure resources
                - **3 resource configurations** (VM, SQL Database, Web App)
                - **Fix templates** for common issues

                ### 🚀 Getting Started

                1. Go to the **Chat Assistant** tab
                2. Try one of the example queries
                3. Or ask your own question!

                ---

                **Version**: 1.0.0 | **Status**: ✅ Running
                """
            )

    # Footer
    gr.HTML(
        """
        <footer>
            <p>Built with ❤️ by <a href="https://github.com/mahimairaja">mahimairaja</a></p>
        </footer>
        """
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
