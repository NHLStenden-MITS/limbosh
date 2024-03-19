from string import whitespace
from input_guards.input_guard import InputGuard, InputGuardFinding


class EmptyInputGuard(InputGuard):
    """ An input guard that detects empty commands.
    """

    def _detect(self, message_content: str) -> bool:
        if len(message_content.strip(whitespace)) == 0:
            return InputGuardFinding.EMPTY_COMMAND
        return InputGuardFinding.OK
        