import gradio as gr
from chatbot import gradio_search

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
