import gradio as gr
from processor import gradio_search, periodic_update
from excel_update import update_job
import threading

update_thread = threading.Thread(target=periodic_update)
update_thread.daemon = True
update_thread.start()

iface = gr.Interface(
    fn=gradio_search, 
    inputs=gr.Textbox(lines=2, placeholder="ask away here"),
    outputs="text",
    title="sage jr",
    description="Looking for someone working on films? SaaS? AI?",
    examples=[
        ["Who's working on AI apps?"],
        ["Find people in data science"],
    ]
)

iface.launch(share=True)
