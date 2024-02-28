""" A simple app that gives you food recommendations based on your mood using ChatGPT.

Authors:
    Saul Johnson (saul.a.johnson@gmail.com)
Since:
    10/12/2023
"""

import json
from typing import Iterable, List
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


# Read config file.
config = None
with open('config.json') as file:
    config = json.load(file)

# Create OpenAI client.
client = OpenAI(api_key=config['openai_api_key'])

# Persist messages in context.
context: List[ChatCompletionMessageParam] = []


def ask_chatgpt (messsages: Iterable[ChatCompletionMessageParam], temperature=0.0001, model="gpt-4"):
    """ Sends a list of chat completion messages to an OpenAI LLM and returns the content of the next message.
    
    Args:
        messages (Iterable[ChatCompletionMessageParam]): Messages currently in context.
        temperature (float): The temperature to use for the LLM.
        model (str): The name of the model to use (e.g. 'gpt-3.5-turbo' or 'gpt-4').
    Returns:
        str: The LLM's response to the prompt.
    """
    return client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messsages
    ).choices[0].message.content
    
def push_context (content: str):
    """ Pushes an additional content message to the LLM context.
    
    Args:
        content (str): The content to push.
    Returns:
        str: The LLM's latest response.
    """
    context.append({'role': 'user', 'content': content}) # Push content in role of user.
    response = ask_chatgpt(context) # Get LLM response.
    context.append({"role": "system", "content": response}) # Push LLM response to context.
    return response


# Add system prompt. This should give us a shell prompt.
prompt = None
with open(config['system_prompt']) as file:
    prompt = push_context(file.read()).strip('` ')


# Loop as a shell until the user exits.
buffer = input(f'{prompt} ')
while buffer != "exit":
    
    # Get LLM response to what's in the buffer.
    reply = push_context(buffer).strip(' `')
    
    # Reply may simply be a prompt, in which case update the prompt.
    if reply.endswith(('#', '$')):
        # Ask for more input using the prompt.
        prompt = reply
        buffer = input(f'{prompt} ')
    else:
        # Print reply then ask for more input using the prompt.
        buffer = input(f'{reply}\n{prompt} ')
