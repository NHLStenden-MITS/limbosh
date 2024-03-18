from typing import List
from input_transformers.input_transformer import InputTransformer
from input_transformers.passthrough_input_transformer import PassthroughInputTransformer


class ChainingInputTransformer(PassthroughInputTransformer):
    """ An input transformer that constructs a chain of responsibility from a list of input transformers.
    """

    def __init__(self, chain: List[InputTransformer]):
        """ Initializes a new instance of an input transformer that constructs a chain of responsibility from a list of input transformrs.

        Args:
            chain (List[InputTransformer]): The list of input transformers to chain together.
        """
        super().__init__(None)

        # Construct chain.
        if len(chain) > 0:
            first_link = self
            latest_link = first_link
            for transformer in chain:
                latest_link.next = transformer
                latest_link = transformer # Remember latest link.
