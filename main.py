from flask import Flask, request
import time
import gradio as gr
from temp import get_response

def user(input, history):
        return gr.update(value="", interactive=False), history + [[input, None]]

def bot(chat_history):
    output = get_response(chat_history[-1][0])
    print(chat_history[-1][0])
    print(output)
    chat_history[-1][1] = ""
    for character in output:
        chat_history[-1][1] += character
        time.sleep(0.05)
        yield chat_history



examples = [
    ["Hello"],
    ["How are you?"],
    ["What's your name?"],
    ["What are your capabilities?"],
    ["Code me a sample AI in Python"]
    ["Is Masturbation bad for health?"]
]


title = """<h1 align="center">BARD Reversed Engineered 💬</h1>"""
custom_css = """
#banner-image {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
#chat-message {
    font-size: 14px;
    min-height: 300px;
}
"""

with gr.Blocks(analytics_enabled=False, css=custom_css) as demo:
    gr.HTML(title)

    history = gr.State([])
    last_user_message = gr.State("")

    with gr.Row():
        with gr.Column():
            gr.Markdown(
                """
            💻 This showcases the reversed engineered and modified version of BARD AI.
    """
            )

    with gr.Row():
        with gr.Box():
            output = gr.Markdown()
            chatbot = gr.Chatbot(elem_id="chat-message", label="Chat")

    with gr.Row():
        with gr.Column(scale=3):
            user_message = gr.Textbox(placeholder="Enter your message here", show_label=False, elem_id="q-input")
            with gr.Row():
                send_button = gr.Button("Send", elem_id="send-btn", visible=True)

                clear_chat_button = gr.Button("Clear chat", elem_id="clear-btn", visible=True)

            with gr.Row():
                gr.Examples(
                    examples=examples,
                    inputs=[user_message],
                    cache_examples=False,
                    fn=get_response,
                    outputs=[output],
                    label="Click on any example and press Enter in the input textbox!",
                )

            with gr.Row():
                gr.Markdown(
                    "Disclaimer: The model can produce factually incorrect output, and should not be relied on to produce "
                    "factually accurate information. The model was trained on various public datasets; while great efforts "
                    "have been taken to clean the pretraining data, it is possible that this model could generate lewd, "
                    "biased, or otherwise offensive outputs.",
                    elem_classes=["disclaimer"],
                )


    response = user_message.submit(user, [user_message, chatbot], [user_message, chatbot], queue=False).then(
            bot, chatbot, chatbot)

    response.then(lambda: gr.update(interactive=True), None, [user_message], queue=False)


    send_btn = send_button.click(user, [user_message, chatbot], [user_message, chatbot], queue=False).then(
            bot, chatbot, chatbot)

    send_btn.then(lambda: gr.update(interactive=True), None, [user_message], queue=False)

    clear_chat_button.click(lambda: None, None, chatbot, queue=False)

        
demo.queue(concurrency_count=16).launch(share=True)
