import gradio as gr
from processor import gradio_search, periodic_update
import threading

update_thread = threading.Thread(target=periodic_update)
update_thread.daemon = True
update_thread.start()

custom_css = """
    body, .gradio-container {
        background-color: #1a1a1a !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        font-family: 'Arial', sans-serif;
        color: white;
    }
    .container {
        max-width: 100% !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
    }
    .main {
        padding: 0 !important;
    }
    #component-0 {
        width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 20px !important;
    }
    .gradio-container .gr-form + .gr-form, .gradio-container .gr-form + .gr-group {
        border-top: none !important;
    }
    .gradio-container .gr-button {
        background-color: #C0C0C0 !important;
        border: 1px solid #A9A9A9 !important;
        color: black !important;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
        padding: 10px 24px;
        transition: background-color 0.3s;
    }
    .gradio-container .gr-button:hover,
    .gradio-container .gr-button.gr-button-lg:hover {
        background-color: #D3D3D3 !important;
    }
    .gr-input {
        font-size: 16px;
        background-color: #2a2a2a;
        border: 1px solid #555555;
        color: white;
        border-radius: 4px;
        padding: 8px;
    }
    .gr-input::placeholder {
        color: #888888;
    }
    .gr-form, .gr-box {
        background-color: #2a2a2a;
        border: 1px solid #555555;
        border-radius: 8px;
        padding: 20px;
    }
    .gr-padded {
        background-color: #2a2a2a;
    }
    h1, h2, h3 {
        color: white;
    }
    p {
        color: #cccccc;
    }
"""

iface = gr.Interface(
    fn=gradio_search, 
    inputs=gr.Textbox(lines=2, placeholder="message sage jr", label=None),
    outputs=gr.Textbox(label="Search Results"),
    title="sage jr",
    description="Looking for someone working on films? SaaS? AI?",
    examples=[
        ["Who's working on AI apps?"],
        ["Find people in data science"],
        ["Who makes content on Instagram?"]
    ],
    css=custom_css
)

iface.launch(share=True)
