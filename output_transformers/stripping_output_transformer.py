from output_transformers.output_transformer import OutputTransformer
from string import whitespace


class StrippingOutputTransformer(OutputTransformer):
    """ An output transformer that returns LLM output with leading and trailing whitespace stripped.
    """

    def _transform(self, message_content: str) -> str:
        return message_content.strip(whitespace)
    