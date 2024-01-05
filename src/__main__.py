"""
Author: Srushanth Baride
Email: Srushanth.Baride@gmail.com
Organization: Intellithing
Date: 13-Dec-2023
Description: A brief description of what the code does.
"""


import os
import torch
import logging
import gradio as gr
from emoji import emojize
from dotenv import load_dotenv
from ctransformers import AutoModelForCausalLM, AutoConfig


# Load variables from .env file
load_dotenv()

# Define constants
MODEL_PATH = os.path.abspath(os.getenv("MODEL_PATH"))
MODEL_FILE = os.getenv("MODEL_FILE")
MODEL_TYPE = os.getenv("MODEL_TYPE")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS"))
CONTEXT_LENGTH = int(os.getenv("CONTEXT_LENGTH"))


# Set up logging
logging.basicConfig(
    level=logging.INFO
)  # Change to logging.ERROR to disable print statements


# Check if GPU acceleration is available and set the number of layers to offload to GPU accordingly
GPU_LAYERS = 150 if torch.cuda.is_available() else 0


def initialize_model():
    """Initialize the language model with the specified model path, file, and type."""
    logging.info("Initializing model...")
    config = AutoConfig.from_pretrained(os.path.join(MODEL_PATH, MODEL_FILE))
    # Explicitly set the max_seq_len
    config.config.max_new_tokens = MAX_NEW_TOKENS
    config.config.context_length = CONTEXT_LENGTH

    return AutoModelForCausalLM.from_pretrained(
        model_path_or_repo_id=MODEL_PATH,
        model_file=MODEL_FILE,
        model_type=MODEL_TYPE,
        gpu_layers=GPU_LAYERS,
        config=config,
    )


def generate_chat_prompt(
    message: str, chat_history: list, single_shot: bool = True
) -> str:
    """
    Generates a chat prompt 🗨️ by iterating over the chat history and appending the new message.

    Args:
        message (str): The new message 💬 to be appended to the chat history.
        chat_history (list): The chat history 📜 as a list of tuples,
        where each tuple contains a pair of strings representing a message and its response.
        single_shot (bool): If True, holds on to the chat history. 🔄

    Returns:
        str: The generated chat prompt as a string. 📝
    """
    if not single_shot:
        # Using list comprehension and join for efficient string concatenation 🚀
        prompt = "\n".join(
            f"[INST] {inst} [/INST]\n{resp}" for inst, resp in chat_history
        )
        # Append the new message to the prompt ➕
        prompt += f"\n[INST] {message} [/INST]"
        # Return the final prompt 🏁
        return prompt
    else:
        return f"[INST] {message} [/INST]"


def generate_bot_response(message: str, chat_history: list):
    """
    Generates a bot response 🤖 by creating a chat prompt, getting the bots message,
    and appending the message and bots response to the chat history.

    Args:
        message (str): The new message 💬 to be appended to the chat history.
        chat_history (list): The chat history 📜 as a list of tuples,
        where each tuple contains a pair of strings representing a message and its response.

    Returns:
        tuple: A tuple containing an empty string and the updated chat history 🔄.
    """
    # Generate a chat prompt using the message and chat history 📝
    generated_prompt = generate_chat_prompt(
        message=message, chat_history=chat_history, single_shot=True
    )

    # Get the bots message by passing the generated prompt to the language model 🧠
    # bot_message = llm(generated_prompt)
    # Stream the output 📡
    bot_message = ""
    for part in llm(generated_prompt, stream=True):
        bot_message += part
        if chat_history:
            chat_history[-1][1] = bot_message
        yield "", chat_history
    # Append the message and bots response to the chat history 📥
    chat_history.append([message, bot_message])


def set_user_response(message: str, chat_history: list) -> tuple:
    """
    Appends the user's message to the chat history and returns the updated chat history. 📝

    Args:
        message (str): The user's message to be appended to the chat history. 💬
        chat_history (list): The current chat history as a list of lists,
        where each inner list contains a pair of strings representing a message and its response. 🗂️

    Returns:
        tuple: A tuple containing the user's message and the updated chat history. 🔄
    """
    # Append the user's message to the chat history 📥
    chat_history.append([message, None])

    # Return the user's message and the updated chat history 📤
    return message, chat_history


def launch_gradio():
    """
    Create a Gradio interface with a chatbot, a textbox, and a clear button and launch the Gradio demo. 🚀
    """
    # Create a Gradio interface with a specific theme 🎨
    with gr.Blocks(
        theme=gr.themes.Default(
            spacing_size=gr.themes.sizes.spacing_sm,
            font=[gr.themes.GoogleFont("Inconsolata"), "Arial", "sans-serif"],
        )
    ) as demo:
        # Initialize the chatbot, textbox, and clear button components 🧩
        chatbot = gr.components.Chatbot(
            label=emojize(":robot: Intellithing's Mistral AI Chatbot")
        )
        msg = gr.components.Textbox(
            label=emojize(":speech_balloon: Enter Your Query to Intellithing's Chatbot")
        )
        clear = gr.components.ClearButton([msg, chatbot])

        # Set the textbox to submit the 'set_user_response' function upon submission
        # Then, generate the bot response 🔄
        msg.submit(set_user_response, [msg, chatbot], [msg, chatbot], queue=False).then(
            generate_bot_response, [msg, chatbot], [msg, chatbot]
        )
        # Clear the chatbot and textbox when the clear button is clicked ❌
        clear.click(lambda: None, None, chatbot, queue=False)

    # Set the maximum size of the queue 📏
    demo.queue(max_size=4 * 1024)
    # Launch the Gradio demo with specific server settings 🌐
    demo.launch(server_name="0.0.0.0", server_port=8080, max_threads=2048)


if __name__ == "__main__":
    # Initialize the language model 🧠
    llm = initialize_model()
    # Launch the Gradio interface 🚀
    launch_gradio()
