import os
import sys
from pathlib import Path

import gradio as gr

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import News_Feeder


def run_news_feeder():
    try:
        News_Feeder.main()
        return "✅ News feeder executed successfully."
    except Exception as exc:
        return f"❌ Error: {exc}"


with gr.Blocks(title="News Feeder Runner") as demo:
    gr.Markdown("# 📩 News Feeder Automation")
    gr.Markdown("Click the button to run the news feeder and generate today's report.")
    btn = gr.Button("Run News Feeder")
    output = gr.Textbox(label="Status")
    btn.click(fn=run_news_feeder, outputs=output)


app = demo


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
    





