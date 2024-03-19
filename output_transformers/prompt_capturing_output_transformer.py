from string import whitespace
from typing import Callable, Optional
from output_transformers.output_transformer import OutputTransformer


class PromptCapturingOutputTransformer(OutputTransformer):
    """ An output transformer that captures and removes the prompt from the LLM output.
    """

    def __init__(self, callback: Optional[Callable[[str], None]] = None, next: OutputTransformer | None = None):
        """ Initializes a new instance of an output transformer that captures and removes the prompt from the LLM output.

        Args:
            callback (Optional[Callable[[str], None]]): The callback to trigger when the prompt changes.
        """
        super().__init__(next)
        self.callback = callback
        self.prompt = None

    def _transform(self, message_content: str) -> str:
        # Split content into lines (preserve line endings).
        message_content_lines = message_content.split('\n')

        # Seek backwards until we find non-empty line. This should be the prompt line.
        offset = -1
        while len(message_content_lines[offset].strip(whitespace)) == 0:
            offset -= 1
            if abs(offset) > len(message_content_lines) and self.prompt is None:
                raise RuntimeError('LLM has deviated. Output consisted only of whitespace, so could not seek prompt.')
        prompt_line = message_content_lines[offset]

        # LLM must always end its output with a prompt.
        if not prompt_line.endswith('$') and self.prompt is None:
            raise RuntimeError(f'LLM has deviated. Output did not end with a prompt (instead, last line was "{prompt_line}").')
        
        # Update prompt and trigger callback if one was provided.
        if prompt_line != self.prompt:
            if self.callback is not None:
                self.callback(prompt_line)
            self.prompt = prompt_line

        # Return message without prompt.
        return '\n'.join(message_content_lines[:offset])
