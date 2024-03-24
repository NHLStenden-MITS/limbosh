from string import whitespace
from output_transformers.output_transformer import OutputTransformer


class LineBreakingOutputTransformer(OutputTransformer):
    """ An output transformer that breaks to the next line if the command yielded output.
    """

    def _transform(self, message_content: str) -> str:
        # Only append a line break if we got output.
        if len(message_content.strip(whitespace)) > 0:
            return f'{message_content}\n'
        return message_content
    