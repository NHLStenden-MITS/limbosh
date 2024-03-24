from joblib import load
from input_guards.input_guard import InputGuard, InputGuardFinding


class TextClassifierInputGuard(InputGuard):
    """ An input guard that uses a text classification model to detect probable prompt injection attacks.
    """
    
    def __init__(self, next: InputGuard | None = None):
        """ Initializes a new instance of an input guard that uses a text classification model to detect probable prompt injection attacks.
        """
        super().__init__(next)
        self.pipeline = load('./models/rf-1-3.model')

    def _detect(self, message_content: str) -> bool:
        if self.pipeline.predict([message_content])[0] == 1:
            return InputGuardFinding.PROBABLE_PROMPT_INJECTION
        return InputGuardFinding.OK
    