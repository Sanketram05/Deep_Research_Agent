import gradio as gr
import os
from dotenv import load_dotenv
from research_manager import ResearchManager
from styles import CSS, JS, EXAMPLES, HEADER_HTML
from agents import set_tracing_disabled

set_tracing_disabled(True)

load_dotenv(override=True)


async def run(email: str, query: str):
    async for status_update in ResearchManager().run(query, email):
        yield status_update


with gr.Blocks(title="Deep Research") as ui:
    gr.HTML(HEADER_HTML)

    email_textbox = gr.Textbox(
        placeholder="Enter your email address...",
        show_label=False,
        container=False,
        elem_id="dr-email",
        elem_classes=["dr-email-input"],
    )

    with gr.Row(elem_classes="dr-query-row"):
        query_textbox = gr.Textbox(
            placeholder="Type a research question...",
            show_label=False,
            container=False,
            autofocus=True,
            elem_id="dr-query",
            scale=5,
        )

        run_button = gr.Button(
            "Investigate",
            variant="primary",
            elem_id="dr-run",
            scale=1
        )

    gr.HTML('<div class="dr-examples-label">Try one</div>')

    gr.Examples(
        examples=EXAMPLES,
        inputs=query_textbox,
        elem_id="dr-examples"
    )

    report = gr.Markdown(elem_id="dr-report")

    run_button.click(
        run,
        inputs=[email_textbox, query_textbox],
        outputs=report
    )

    query_textbox.submit(
        run,
        inputs=[email_textbox, query_textbox],
        outputs=report
    )


if __name__ == "__main__":
    ui.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base()
    )