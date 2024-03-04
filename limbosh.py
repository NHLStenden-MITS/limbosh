""" The honeypot shell that traps you in a conversation with an LLM pretending to be a shell.

Authors:
    Saul Johnson (saul.johnson@nhlstenden.com)
Since:
    28/02/2023
"""

import json
from typing import List

from llm.large_language_model import LargeLanguageModel, ChatMessage
from llm.openai_large_language_model import OpenaiLargeLanguageModel


# Read config file.
config = None
with open('config.json') as file:
    config = json.load(file)

# Create OpenAI client.
llm: LargeLanguageModel = OpenaiLargeLanguageModel(config['openai_api_key'])

# Persist messages in context.
context: List[ChatMessage] = []

    
def push_context (content: str):
    """ Pushes an additional content message to the LLM context.
    
    Args:
        content (str): The content to push.
    Returns:
        str: The LLM's latest response.
    """
    context.append(ChatMessage('user', content)) # Push content in role of user.
    response = llm.get_next_message(context) # Get LLM response.
    context.append(response) # Push LLM response to context.
    return response.content


# Add system prompt. This should give us a shell prompt.
prompt = None
with open(config['system_prompt']) as file:
    prompt = push_context(file.read()).strip('` ')


# Loop as a shell until the user exits.
buffer = input(f'{prompt} ')
while buffer != "exit":
    
    # Get LLM response to what's in the buffer.
    reply = push_context(buffer).strip(' `\n\r')
    reply_lines = reply.split('\n')
    
    # Reply may simply be a prompt, in which case update the prompt.
    if reply.endswith(('#', '$')):
        # Ask for more input using the prompt.
        prompt = reply_lines[-1].strip(' `\n\r')
        reply_exluding_prompt = "\n".join(reply_lines[:-1])
        buffer = input(f'{reply_exluding_prompt}\n{prompt} ')
    else:
        # Print reply then ask for more input using the prompt.
        buffer = input(f'{reply}\n{prompt} ')
