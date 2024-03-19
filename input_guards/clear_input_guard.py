from string import whitespace
from input_guards.input_guard import InputGuard, InputGuardFinding


class ClearInputGuard(InputGuard):
    """ An input guard that detects console clear commands.
    """

    def _detect(self, message_content: str) -> bool:
        if message_content.strip(whitespace) == 'clear':
            return InputGuardFinding.SPECIAL_COMMAND_CLEAR
        return InputGuardFinding.OK
        