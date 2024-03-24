from typing import Dict, Literal

from kink import inject

from config.config_provider import ConfigProvider
from input_transformers.chaining_input_transformer import ChainingInputTransformer
from input_transformers.delimiting_input_transformer import DelimitingInputTransformer
from input_transformers.input_transformer import InputTransformer
from input_transformers.passthrough_input_transformer import PassthroughInputTransformer


@inject
class InputTransformerFactory():
    """ A factory for creating input transformer instances depending on application-level configuration.
    """

    def __init__(self, config_provider: ConfigProvider):
        """ Initializes a new instance of a factory for creating input transformer instances depending on application-level configuration.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
        """
        self.config = config_provider.get()

    @staticmethod
    def construct(input_transformer_type: Literal['passthrough', 'delimiting']) -> InputTransformer:
        """ Constructs an input transformer based on its type token.

        Args:
            input_transformer_type (Literal['passthrough', 'delimiting']): The type token of the desired input transformer.
        Returns:
            InputGuard: An instance of the desired input transformer.
        """
        if input_transformer_type == 'passthrough':
            return PassthroughInputTransformer()
        if input_transformer_type == 'delimiting':
            return DelimitingInputTransformer()
        raise NameError(f'Input transformer "{input_transformer_type}" unknown or not supported.')

    def get(self):
        """ Returns a newly-constructed input transformer instance based on the application configuration passed.

        Returns:
            InputTransformer: The newly-constructed input transformer.
        """
        return ChainingInputTransformer([InputTransformerFactory.construct(input_transformer) for input_transformer in self.config.input_transformers])
