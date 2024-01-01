import os
import gradio as gr
from ctransformers import AutoModelForCausalLM
from ctransformers import AutoConfig

import torch
print("*"*50)
print(os.path.abspath("./model_gguf"))
print("*"*50)


config = AutoConfig.from_pretrained(os.path.abspath("./model_gguf/mistral-7b-instruct-v0.1.Q5_K_M.gguf"))
# Explicitly set the max_seq_len
config.config.max_new_tokens = 2048
config.config.context_length = 4096

# Check if GPU acceleration is available and set the number of layers to offload to GPU accordingly
gpu_layers = 50 if torch.cuda.is_available() else 0
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Initialize the language model with the specified model path, file, and type
llm = AutoModelForCausalLM.from_pretrained(model_path_or_repo_id=os.path.abspath("./model_gguf/"),
                                           model_file="mistral-7b-instruct-v0.1.Q5_K_M.gguf",
                                           model_type="mistral",
                                           gpu_layers=100,
                                           config=config)

llm = llm.to(device)



def generate_chat_prompt(message: str, chat_history: list, single_shot: bool = True) -> str:
    """
    Generates a chat prompt by iterating over the chat history and appending the new message.

    Args:
        message (str): The new message to be appended to the chat history.
        chat_history (list): The chat history as a list of tuples,
        where each tuple contains a pair of strings representing a message and its response.
        single_shot (bool): If True, holds on to the chat history.

    Returns:
        str: The generated chat prompt as a string.
    """
    if not single_shot:
        # Initialize an empty string for the prompt
        prompt = ""

        # Iterate over the chat history
        for inst, resp in chat_history:
            # For each pair in the history, append the instruction and response to the prompt
            prompt += f"[INST] {inst} [/INST]\n{resp}\n"

        # Append the new message to the prompt
        prompt += f"[INST] {message} [/INST]"

        # Return the final prompt
        return prompt
    else:
        return f"[INST] {message} [/INST]"


def generate_bot_response(message: str, chat_history: list):
    """
    Generates a bot response by creating a chat prompt, getting the bots message,
    and appending the message and bots response to the chat history.

    Args:
        message (str): The new message to be appended to the chat history.
        chat_history (list): The chat history as a list of tuples,
        where each tuple contains a pair of strings representing a message and its response.

    Returns:
        tuple: A tuple containing an empty string and the updated chat history.
    """
    # Generate a chat prompt using the message and chat history
    generated_prompt = generate_chat_prompt(message=message, chat_history="chat_history", single_shot=True)

    # Get the bots message by passing the generated prompt to the language model
    # bot_message = llm(generated_prompt)
    # Stream the output
    l = ""
    for bot_message in llm(generated_prompt, stream=True):
        l += bot_message
        chat_history[-1][1] = l
        yield "", chat_history
    chat_history.append([message, bot_message])


def set_user_response(message: str, chat_history: list) -> tuple:
    chat_history += [[message, None]]
    return message, chat_history
        

    # # Append the message and bots response to the chat history
    # chat_history.append((message, bot_message))

    # # Return an empty string and the updated chat history
    # return "", chat_history


# Create a Gradio interface with a chatbot, a textbox, and a clear button
with gr.Blocks(theme=gr.themes.Default(spacing_size=gr.themes.sizes.spacing_sm, 
                                       # radius_size=gr.themes.sizes.radius_none, 
                                       font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"])) as demo:
    chatbot = gr.components.Chatbot(label="Mistral AI")
    msg = gr.components.Textbox(label="User query")
    clear = gr.components.ClearButton([msg, chatbot])

    # Set the textbox to submit the 'generate_bot_response' function upon submission
    msg.submit(set_user_response, 
               [msg, chatbot], 
               [msg, chatbot], 
               queue=False).then(generate_bot_response, 
                                 [msg, chatbot], 
                                 [msg, chatbot])
    # submit_button.click(fn=generate_bot_response, 
    #                     inputs=[msg, chatbot], 
    #                     outputs=[msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the Gradio demo


if __name__ == "__main__":
    demo.queue(max_size=1024)
    demo.launch(server_name="0.0.0.0", server_port=8080, max_threads=2048)
