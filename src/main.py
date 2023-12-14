import gradio as gr
from ctransformers import AutoModelForCausalLM

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained("../model_gguf/",
                                           model_file="mistral-7b-instruct-v0.1.Q5_K_M.gguf",
                                           model_type="mistral",
                                           # gpu_layers=50
                                           )


def ch(message, chat_history):
    prompt = ""
    for i, j in chat_history:
        prompt += f"[INST] {i} [/INST]"
        prompt += f"\n{j}\n"
    prompt += f"[INST] {message} [/INST]"
    return llm(prompt)


if __name__ == "__main__":
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])


        def respond(message, chat_history):
            bot_message = ch(message, chat_history)
            chat_history.append((message, bot_message))
            return "", chat_history


        msg.submit(respond, [msg, chatbot], [msg, chatbot])

    demo.launch(share=False)
