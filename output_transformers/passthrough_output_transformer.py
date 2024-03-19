from output_transformers.output_transformer import OutputTransformer


class PassthroughOutputTransformer(OutputTransformer):
    """ An output transformer that returns LLM output unchanged.
    """

    def _transform(self, message_content: str) -> str:
        # Return input unchanged.
        return message_content
    