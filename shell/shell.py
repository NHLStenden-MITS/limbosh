from logging import Logger
import os
import platform
import sys
from typing import Iterable, List

from kink import inject

from config.config_provider import ConfigProvider
from input_guards.input_guard import InputGuardFinding
from input_guards.input_guard_factory import InputGuardFactory
from input_transformers.input_transformer_factory import InputTransformerFactory
from llm.context_compressor import ContextCompressor
from llm.large_language_model import ChatMessage
from llm.large_language_model_factory import LargeLanguageModelFactory
from output_guards.output_guard import OutputGuardFinding
from output_guards.output_guard_factory import OutputGuardFactory
from output_transformers.output_transformer_factory import OutputTransformerFactory
from prompting.prompt_factory import PromptFactory


@inject
class Shell():
    """ Represents an LLM-powered honeypot shell.
    """

    def __init__(
            self,
            config_provider: ConfigProvider,
            large_language_model_factory: LargeLanguageModelFactory, 
            context_compressor: ContextCompressor,
            prompt_factory: PromptFactory,
            input_guard_factory: InputGuardFactory, 
            input_transformer_factory: InputTransformerFactory,
            output_guard_factory: OutputGuardFactory,
            output_transformer_factory: OutputTransformerFactory,
            logger: Logger):
        """ Intitializes a new instance of an LLM-powered honeypot shell.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
            large_language_model_factory (LargeLanguageModelFactory): The LLM factory to use to generate an LLM instance.
            context_compressor (ContextCompressor): The context compressor to use to expand the functional context window width of the LLM.
            prompt_factory (PromptFactory): The prompt factory to use to generate the system prompt.
            input_guard_factory (InputGuardFactory): The input guard factory to generate an input guard for the LLM.
            input_transformer_factory (InputGuardFactory): The input transformer factory to generate an input transformer for the LLM.
            output_guard_factory (OutputGuardFactory): The output guard factory to generate an output guard for the LLM.
            output_transformer_factory (OutputTransformerFactory): The output transformer factory to generate an output transformer for the LLM.
            logger (Logger): The logger to use for this instance.
        """
        self.config_provider = config_provider.get()
        self.large_language_model = large_language_model_factory.get()
        self.context_compressor = context_compressor
        self.system_prompt = prompt_factory.get(self.config_provider.shell)
        self.input_guard = input_guard_factory.get()
        self.input_transformer = input_transformer_factory.get()
        self.output_guard = output_guard_factory.get()
        self.output_transformer = output_transformer_factory.get(lambda new_prompt: self.update_prompt(new_prompt))
        self.logger = logger

        # Set default prompt.
        self.prompt = '$'

        # Initialize context to empty.
        context: List[ChatMessage] = []
        self.context = context

        # Initialize context compression boundary.
        self.context_compression_boundary: int | None = None

    @staticmethod
    def _estimate_tokens_in_str (str) -> int:
        """ Provides a rough estimate of the number of tokens in a string.

        Uses the algorithm here: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        
        Returns:
            int: The estimated number of tokens in the string provided.
        """
        return len(str) // 4

    def _estimate_tokens (self) -> int:
        """ Provides a rough estimate of the number of tokens in the shell's context window.
        
        Returns:
            int: The estimated number of tokens in the shell's context window.
        """
        return sum([Shell._estimate_tokens_in_str(message.content) for message in self.context]) // 4

    def push_context (self, content: str, transform_input: bool = True, transform_output = True):
        """ Pushes an additional content message to the LLM context.
        
        Args:
            content (str): The content to push.
            transform_input (bool): Whether to transform the content prior to pushing it to the context (default true).
            transform_output (bool): Whether to transform LLM output prior to pushing it to the context (default true).
        Returns:
            str: The LLM's latest response.
        """
        self.logger.debug(f"Pushing message {len(self.context)} to the context. Message length is approx. {Shell._estimate_tokens_in_str(content)} tokens.")

        # Transform input if specified.
        final_content = content
        if transform_input:
            final_content = self.input_transformer.transform(content)
            self.logger.debug(f"Message transformed to contain approx. {Shell._estimate_tokens_in_str(final_content)} tokens.")

        # Push content in role of user.
        self.context.append(ChatMessage('user', final_content))

        # Get LLM response.
        response = self.large_language_model.get_next_message(self.context)
        self.logger.debug(f"LLM responded with approx. {Shell._estimate_tokens_in_str(response.content)} tokens.")

        # Transform output if specified.
        if transform_output:
            response.content = self.output_transformer.transform(response.content)
            self.logger.debug(f"LLM output transformed to contain approx. {Shell._estimate_tokens_in_str(response.content)} tokens.")

        # Push LLM response to context and return.
        self.context.append(response)
        self.logger.debug(f"Context size now stands at approx. {self._estimate_tokens()} tokens.")
        return response.content

    def update_prompt (self, new_prompt: str):
        """ An event handler invoked by the prompt capturing output transformer when the prompt changes.

        Args:
            new_prompt (str): The new prompt.
        """
        self.prompt = new_prompt

    def _context_compressor_callback (self, chat_messages: Iterable[ChatMessage]):
        """ A callback invoked by the context compressor when context compression has finished.

        Args:
            chat_messages (Iterable[ChatMessage]): The compressed chat messages.
        """
        self.context = [*chat_messages, *self.context[self.context_compression_boundary + 1:]]
        self.context_compression_boundary = None
        self.logger.debug(f'Finished compressing context. Ending length approx. {self._estimate_tokens()} tokens.')

    def run(self):
        """ Enters the shell.
        """

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
                output = self.push_context(buffer)
                output_guard_finding = self.output_guard.detect(buffer, output) # Run through output guard.
                if output_guard_finding == OutputGuardFinding.OK:

                    # All OK, print output.
                    print(output, end='')
                elif output_guard_finding == OutputGuardFinding.PROBABLE_DEVIATION:
                    
                    # Simply force a disconnect (context will reset).
                    sys.exit(0)
            elif input_guard_finding == InputGuardFinding.SPECIAL_COMMAND_EXIT:

                # Terminate program.
                sys.exit(0)
            elif input_guard_finding == InputGuardFinding.SPECIAL_COMMAND_CLEAR:

                # Clear terminal (platform-dependent).
                if platform.system() == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')
            elif input_guard_finding == InputGuardFinding.PROBABLE_PROMPT_INJECTION:

                # Do not allow dangerous input to proceed to LLM.
                print(f"{buffer.split(' ')[0]}: Command not found")

            # Compress context in background.
            if self.context_compression_boundary is None and self._estimate_tokens() > self.config_provider.context_compression_threshold:
                self.logger.debug(f'Compressing context in background. Starting length approx. {self._estimate_tokens()} tokens.')
                self.context_compression_boundary = len(self.context)
                self.context_compressor.compress(self.context, self._context_compressor_callback)
