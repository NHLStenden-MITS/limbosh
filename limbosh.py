""" The honeypot shell that traps you in a conversation with an LLM pretending to be a shell.

Authors:
    Saul Johnson (saul.johnson@nhlstenden.com)
Since:
    28/02/2023
"""

from string import Template
import json
from typing import List
from input_guards.input_guard_factory import InputGuardFactory
from input_transformers.input_transformer import InputTransformer
from input_transformers.input_transformer_factory import InputTransformerFactory

from llm.large_language_model import LargeLanguageModel, ChatMessage
from llm.large_language_model_factory import LargeLanguageModelFactory
from output_transformers.output_transformer import OutputTransformer
from output_transformers.output_transformer_factory import OutputTransformerFactory


# Read config file.
config = None
with open('config.json') as file:
    config = json.load(file)

# Maintain shell prompt.
prompt: str | None = None

# Create LLM instance.
llm: LargeLanguageModel = LargeLanguageModelFactory.get(config)

# Input guards.
input_guard: InputTransformer = InputGuardFactory.get(config)

# Input transformers.
input_transformer: InputTransformer = InputTransformerFactory.get(config)

# Output transformers.
def update_prompt (new_prompt: str):
    global prompt
    prompt = new_prompt
output_transformer: OutputTransformer = OutputTransformerFactory.get(config, prompt_changed_callback=update_prompt)

# Persist messages in context.
context: List[ChatMessage] = []

    
def push_context (content: str, transform_input: bool = True):
    """ Pushes an additional content message to the LLM context.
    
    Args:
        content (str): The content to push.
        transform_input (bool): Whether to transform the content prior to pushing it to the context (default true).
    Returns:
        str: The LLM's latest response.
    """
    final_content = input_transformer.transform(content) if transform_input else content
    context.append(ChatMessage('user', final_content)) # Push content in role of user.
    response = llm.get_next_message(context) # Get LLM response.
    response.content = output_transformer.transform(response.content)
    context.append(response) # Push LLM response to context.
    return response.content


# Input system prompt.
with open(config['system_prompt']) as file:
    template = Template(file.read())
    push_context(template.substitute(config['prompt']), transform_input=False)


# Loop as a shell until the user exits.
buffer = input(f'{prompt} ')
while buffer != "exit":
    
    # Get LLM response to what's in the buffer.
    reply = push_context(buffer)

    # Sometimes the LLM echoes back our input. Remove this.
    if reply.startswith(buffer):
        reply = reply[len(buffer):]

    reply_lines = reply.split('\n')
    
    # Reply may simply be a prompt, in which case update the prompt.
    if reply.endswith(('#', '$')):
        # Ask for more input using the prompt.
        prompt = reply_lines[-1]
        reply_exluding_prompt = "\n".join(reply_lines[:-1])
        buffer = input(f'{reply_exluding_prompt}\n{prompt} ')
    else:
        # Print reply then ask for more input using the prompt.
        buffer = input(f'{reply}\n{prompt} ')
