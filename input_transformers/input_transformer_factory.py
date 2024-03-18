from typing import Dict, Literal

from input_transformers.chaining_input_transformer import ChainingInputTransformer
from input_transformers.delimiting_input_transformer import DelimitingInputTransformer
from input_transformers.input_transformer import InputTransformer
from input_transformers.passthrough_input_transformer import PassthroughInputTransformer


class InputTransformerFactory():
    """ A static factory for creating input transformer instances depending on application-level configuration.
    """

    @staticmethod
    def construct(input_transformer_type: Literal['passthrough', 'delimiting']) -> InputTransformer:
        if input_transformer_type == 'passthrough':
            return PassthroughInputTransformer()
        if input_transformer_type == 'delimiting':
            return DelimitingInputTransformer()
        raise NameError(f'Input transformer "{input_transformer_type}" unknown or not supported.')

    @classmethod
    def get(cls, configuration: Dict[str, str]):
        """ Returns a newly-constructed input transformer instance based on the application configuration passed.

        Args:
            configuration (Dict[str, str]): The application configuration dictionary.
        Returns:
            InputTransformer: The newly-constructed input transformer.
        """
        config = configuration["input_transformers"]
        if type(config) is str:
            return cls.construct(config)
        return ChainingInputTransformer([cls.construct(input_transformer) for input_transformer in config])
