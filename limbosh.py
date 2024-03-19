""" The honeypot shell that traps you in a conversation with an LLM pretending to be a shell.

Authors:
    Saul Johnson (saul.johnson@nhlstenden.com)
Since:
    28/02/2023
"""

import os
import platform
from string import Template
import json
from typing import List
from input_guards.input_guard import InputGuard, InputGuardFinding
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
input_guard: InputGuard = InputGuardFactory.get(config)

# Input transformers.
input_transformer: InputTransformer = InputTransformerFactory.get(config)

# Output transformers.
def update_prompt (new_prompt: str):
    """ An event handler invoked by the prompt capturing output transformer when the prompt changes.

    Args:
        new_prompt (str): The new prompt.
    """
    global prompt
    prompt = new_prompt
output_transformer: OutputTransformer = OutputTransformerFactory.get(config, prompt_changed_callback=update_prompt)

# Persist messages in context.
context: List[ChatMessage] = []

    
def push_context (content: str, transform_input: bool = True, transform_output = True):
    """ Pushes an additional content message to the LLM context.
    
    Args:
        content (str): The content to push.
        transform_input (bool): Whether to transform the content prior to pushing it to the context (default true).
        transform_output (bool): Whether to transform LLM output prior to pushing it to the context (default true).
    Returns:
        str: The LLM's latest response.
    """
    # Transform input if specified.
    final_content = input_transformer.transform(content) if transform_input else content

     # Push content in role of user.
    context.append(ChatMessage('user', final_content))

    # Get LLM response.
    response = llm.get_next_message(context)

    # Transform output if specified.
    if transform_output:
        response.content = output_transformer.transform(response.content)

    # Push LLM response to context and return.
    context.append(response)
    return response.content


# Input system prompt.
with open(config['system_prompt']) as file:
    template = Template(file.read())
    filled_prompt = template.substitute(config['prompt']) # Substitute template variables.
    push_context(filled_prompt, transform_input=False)


# Loop as a shell until the user exits.
reply = None
while True:

    # Print output (if any) and read next command into buffer.
    buffer = input(f'{reply if reply is not None else ''}{prompt} ')
    
    # Run input through guard.
    input_guard_finding = input_guard.detect(buffer)
    if input_guard_finding == InputGuardFinding.OK:

        # Get LLM response to what's in the buffer.
        reply = push_context(buffer)
    elif input_guard_finding == InputGuardFinding.SPECIAL_COMMAND_EXIT:

        # Break out of loop (program will terminate).
        break
    elif input_guard_finding == InputGuardFinding.SPECIAL_COMMAND_CLEAR:

        # Clear terminal (platform-dependent).
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
