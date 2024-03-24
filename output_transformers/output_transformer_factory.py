from typing import Callable, Dict, Literal, Optional

from kink import inject

from config.config_provider import ConfigProvider
from output_transformers.chaining_output_transformer import ChainingOutputTransformer
from output_transformers.line_breaking_output_transformer import LineBreakingOutputTransformer
from output_transformers.output_transformer import OutputTransformer
from output_transformers.passthrough_output_transformer import PassthroughOutputTransformer
from output_transformers.prompt_capturing_output_transformer import PromptCapturingOutputTransformer
from output_transformers.stripping_output_transformer import StrippingOutputTransformer


@inject
class OutputTransformerFactory():
    """ A factory for creating output transformer instances depending on application-level configuration.
    """

    def __init__(self, config_provider: ConfigProvider):
        """ Initializes a new instance of a factory for creating output transformer instances depending on application-level configuration.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
        """
        self.config = config_provider.get()

    @staticmethod
    def construct(output_transformer_type: Literal['passthrough', 'stripping', 'line_breaking']) -> OutputTransformer:
        if output_transformer_type == 'passthrough':
            return PassthroughOutputTransformer()
        if output_transformer_type == 'stripping':
            return StrippingOutputTransformer()
        if output_transformer_type == 'line_breaking':
            return LineBreakingOutputTransformer()
        raise NameError(f'Output transformer "{output_transformer_type}" unknown or not supported.')

    def get(self, prompt_changed_callback: Optional[Callable[[str], None]] = None):
        """ Returns a newly-constructed output transformer instance based on the application configuration passed.

        Args:
            prompt_changed_callback (Optional[Callable[[str], None]]): The callback to trigger when the shell prompt changes.
        Returns:
            OutputTransformer: The newly-constructed output transformer.
        """
        config = self.config.output_transformers
        if type(config) is str:
            return OutputTransformerFactory.construct(config)
        return ChainingOutputTransformer([
            PromptCapturingOutputTransformer(callback=prompt_changed_callback), # Hard-code prompt capturing transformer.
            *[OutputTransformerFactory.construct(output_transformer) for output_transformer in config]
        ])
