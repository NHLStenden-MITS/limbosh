from typing import List
from output_transformers.output_transformer import OutputTransformer
from output_transformers.passthrough_output_transformer import PassthroughOutputTransformer


class ChainingOutputTransformer(PassthroughOutputTransformer):
    """ An output transformer that constructs a chain of responsibility from a list of output transformers.
    """

    def __init__(self, chain: List[OutputTransformer]):
        """ Initializes a new instance of an output transformer that constructs a chain of responsibility from a list of output transformrs.

        Args:
            chain (List[OutputTransformer]): The list of output transformers to chain together.
        """
        super().__init__(None)

        # Construct chain.
        if len(chain) > 0:
            first_link = self
            latest_link = first_link
            for transformer in chain:
                latest_link.next = transformer
                latest_link = transformer # Remember latest link.
