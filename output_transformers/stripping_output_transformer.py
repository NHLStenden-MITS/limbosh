from functools import reduce
from output_transformers.output_transformer import OutputTransformer
from string import whitespace


class StrippingOutputTransformer(OutputTransformer):
    """ An output transformer that returns LLM output with leading and trailing whitespace stripped.
    """

    def _transform(self, message_content: str) -> str:
        chars_to_strip = [whitespace, '`', whitespace]
        buffer = message_content
        for char_to_strip in chars_to_strip:
            buffer = buffer.strip(char_to_strip)
        return buffer
    