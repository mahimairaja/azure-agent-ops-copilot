import gradio as gr

app = gr.Blocks()

with app:
    gr.Markdown("# Azure Agent Ops Copilot")

if __name__ == "__main__":
    app.launch()
