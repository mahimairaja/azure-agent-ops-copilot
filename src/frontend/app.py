import os

import gradio as gr
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")


def chat(message, history):
    try:
        response = requests.post(f"{API_URL}/chat", json={"message": message})
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(title="Azure Ops Copilot") as demo:
    gr.Markdown("# 🤖 Azure Ops Copilot")
    gr.Markdown(
        "Your AI assistant for Azure DevOps. Ask me to analyze alerts, check configs, or suggest fixes."
    )

    chatbot = gr.ChatInterface(
        fn=chat,
        examples=[
            "Analyze alert alert-001",
            "Check config for vm-01",
            "Suggest a fix for high CPU on vm-01",
        ],
        title="Chat with Copilot",
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
