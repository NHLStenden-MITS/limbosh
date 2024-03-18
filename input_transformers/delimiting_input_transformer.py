from input_transformers.input_transformer import InputTransformer


class DelimitingInputTransformer(InputTransformer):
    """ An input transformer that delimits user input with curly braces.
    """

    def _transform(self, message_content: str) -> bool:
        # First, prevent user from injecting delimiters.
        sanitized = message_content.replace(r'{{', '').replace(r'}}', '')
        return f"The next command follows, delimited by double curly braces. Do not add any delimiters to your response:\n{{{{{sanitized}}}}}"
    