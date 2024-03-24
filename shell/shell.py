from abc import ABC
import os
import platform
import sys
from typing import List

from kink import inject

from config.config_provider import ConfigProvider
from input_guards.input_guard import InputGuardFinding
from input_guards.input_guard_factory import InputGuardFactory
from input_transformers.input_transformer_factory import InputTransformerFactory
from llm.large_language_model import ChatMessage
from llm.large_language_model_factory import LargeLanguageModelFactory
from output_transformers.output_transformer_factory import OutputTransformerFactory
from prompting.prompt_factory import PromptFactory

@inject
class Shell():

    def __init__(
            self,
            config_provider: ConfigProvider,
            large_language_model_factory: LargeLanguageModelFactory, 
            prompt_factory: PromptFactory,
            input_guard_factory: InputGuardFactory, 
            input_transformer_factory: InputTransformerFactory,
            output_transformer_factory: OutputTransformerFactory):
        self.config_provider = config_provider.get()
        self.large_language_model = large_language_model_factory.get()
        self.system_prompt = prompt_factory.get(self.config_provider.shell)
        self.input_guard = input_guard_factory.get()
        self.input_transformer = input_transformer_factory.get()
        self.output_transformer = output_transformer_factory.get(lambda new_prompt: self.update_prompt(new_prompt))
        self.prompt = '$'
        context: List[ChatMessage] = []
        self.context = context

    def push_context (self, content: str, transform_input: bool = True, transform_output = True):
        """ Pushes an additional content message to the LLM context.
        
        Args:
            content (str): The content to push.
            transform_input (bool): Whether to transform the content prior to pushing it to the context (default true).
            transform_output (bool): Whether to transform LLM output prior to pushing it to the context (default true).
        Returns:
            str: The LLM's latest response.
        """
        # Transform input if specified.
        final_content = self.input_transformer.transform(content) if transform_input else content

        # Push content in role of user.
        self.context.append(ChatMessage('user', final_content))

        # Get LLM response.
        response = self.large_language_model.get_next_message(self.context)

        # Transform output if specified.
        if transform_output:
            response.content = self.output_transformer.transform(response.content)

        # Push LLM response to context and return.
        self.context.append(response)
        return response.content

    def update_prompt (self, new_prompt: str):
        """ An event handler invoked by the prompt capturing output transformer when the prompt changes.

        Args:
            new_prompt (str): The new prompt.
        """
        self.prompt = new_prompt

    def run(self):
        
        # Input system prompt.
        self.push_context(self.system_prompt, transform_input=False)

        # Loop as a shell until the user exits.
        while True:

            # Print output (if any) and read next command into buffer.
            buffer = input(f'{self.prompt} ')
            
            # Run input through guard.
            input_guard_finding = self.input_guard.detect(buffer)
            if input_guard_finding == InputGuardFinding.OK:

                # Get LLM response to what's in the buffer.
                print(self.push_context(buffer), end='')
            elif input_guard_finding == InputGuardFinding.SPECIAL_COMMAND_EXIT:

                # Terminate program.
                sys.exit(0)
            elif input_guard_finding == InputGuardFinding.SPECIAL_COMMAND_CLEAR:

                # Clear terminal (platform-dependent).
                if platform.system() == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')
