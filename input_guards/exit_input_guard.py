from string import whitespace
from input_guards.input_guard import InputGuard, InputGuardFinding


class ExitInputGuard(InputGuard):
    """ An input guard that detects exit commands.
    """

    def _detect(self, message_content: str) -> bool:
        if message_content.strip(whitespace) == 'exit':
            return InputGuardFinding.SPECIAL_COMMAND_EXIT
        return InputGuardFinding.OK
        