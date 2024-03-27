from typing import Literal

from kink import inject

from config.config_provider import ConfigProvider
from llm.large_language_model_factory import LargeLanguageModelFactory
from output_guards.appropriateness_output_guard import AppropriatenessOutputGuard
from output_guards.chaining_output_guard import ChainingOutputGuard
from output_guards.output_guard import OutputGuard
from output_guards.passthrough_output_guard import PassthroughOutputGuard
from prompting.prompt_factory import PromptFactory


@inject
class OutputGuardFactory():
    """ A factory for creating output guard instances depending on application-level configuration.
    """

    def __init__(self, config_provider: ConfigProvider, large_language_model_factory: LargeLanguageModelFactory, prompt_factory: PromptFactory):
        """ Initializes a new instance of a factory for creating output guard instances depending on application-level configuration.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
            large_language_model_factory (LargeLanguageModelFactory): The LLM factory to use to generate any LLM instances required.
            prompt_factory (PromptFactory): The prompt factory to use to generate any prompts required.
        """
        self.config = config_provider.get()
        self.large_language_model_factory = large_language_model_factory
        self.prompt_factory = prompt_factory

    def construct(self, output_guard_type: Literal['passthrough', 'appropriateness']) -> OutputGuard:
        """ Constructs an output guard based on its type token.

        Args:
            output_guard_type (Literal['passthrough']): The type token of the desired output guard.
        Returns:
            OutputGuard: An instance of the desired output guard.
        """
        if output_guard_type == 'passthrough':
            return PassthroughOutputGuard()
        if output_guard_type == 'appropriateness':
            return AppropriatenessOutputGuard(self.prompt_factory, self.large_language_model_factory)
        raise NameError(f'Output guard "{output_guard_type}" unknown or not supported.')

    def get(self):
        """ Returns a newly-constructed output guard instance based on application-level configuration.

        Returns:
            OutputGuard: The newly-constructed output guard.
        """
        return ChainingOutputGuard([self.construct(output_guard) for output_guard in self.config.output_guards])
