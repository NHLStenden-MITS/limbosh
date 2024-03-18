from input_transformers.input_transformer import InputTransformer


class PassthroughInputTransformer(InputTransformer):
    """ An input transformer that returns user input unchanged.
    """

    def _transform(self, message_content: str) -> bool:
        return message_content
    