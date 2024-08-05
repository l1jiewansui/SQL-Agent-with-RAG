import gradio as gr
 
def show_text(text):
    print(text)
    return text
 
interface = gr.Interface(show_text, "text", "text")
interface.launch(server_name="0.0.0.0", share=True)