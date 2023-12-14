import os
import gradio as gr
from ctransformers import AutoModelForCausalLM

import torch
print("*"*50)
print(os.path.abspath("./model_gguf/"))
print("*"*50)

# Check if GPU acceleration is available and set the number of layers to offload to GPU accordingly
gpu_layers = 50 if torch.cuda.is_available() else 0


# Initialize the language model with the specified model path, file, and type
llm = AutoModelForCausalLM.from_pretrained(model_path_or_repo_id=os.path.abspath("./model_gguf/"),
                                           model_file="mistral-7b-instruct-v0.1.Q5_K_M.gguf",
                                           model_type="mistral",
                                           gpu_layers=gpu_layers)


def generate_chat_prompt(message: str, chat_history: list) -> str:
    """
    Generates a chat prompt by iterating over the chat history and appending the new message.

    Args:
        message (str): The new message to be appended to the chat history.
        chat_history (list): The chat history as a list of tuples,
        where each tuple contains a pair of strings representing a message and its response.

    Returns:
        str: The generated chat prompt as a string.
    """
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


def generate_bot_response(message: str, chat_history: list) -> tuple:
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
    generated_prompt = generate_chat_prompt(message=message, chat_history=chat_history)

    # Get the bots message by passing the generated prompt to the language model
    bot_message = llm(generated_prompt)

    # Append the message and bots response to the chat history
    chat_history.append((message, bot_message))

    # Return an empty string and the updated chat history
    return "", chat_history


def main():
    """
    Main function to initialize the language model, create the Gradio interface, and launch the demo.

    The function first checks if GPU acceleration is available and sets the number of
    layers to offload to GPU accordingly.
    It then initializes the language model with the specified model path, file, and type.
    After that, it creates a Gradio interface with a chatbot, a textbox, and a clear button.
    It sets the textbox to submit the 'generate_bot_response' function upon submission.
    Finally, it launches the Gradio demo.
    """

    # Create a Gradio interface with a chatbot, a textbox, and a clear button
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        _clear = gr.ClearButton([msg, chatbot])

        # Set the textbox to submit the 'generate_bot_response' function upon submission
        msg.submit(generate_bot_response, [msg, chatbot], [msg, chatbot])

    # Launch the Gradio demo
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
