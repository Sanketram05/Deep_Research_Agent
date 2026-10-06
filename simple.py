import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str, email: str):
    async for status_update in ResearchManager().run(query,email):
        yield status_update


with gr.Blocks() as ui:
    email_textbox = gr.Textbox(
    label="Email",
    placeholder="Enter your email address",
    type="email"
    )
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    
    run_button.click(run, inputs=[query_textbox, email_textbox], outputs=report)
    query_textbox.submit(run, inputs=[query_textbox, email_textbox], outputs=report)

ui.launch(theme=gr.themes.Default(primary_hue="sky"))

