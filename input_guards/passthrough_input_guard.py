from input_guards.input_guard import InputGuard, InputGuardFinding


class PassthroughInputGuard(InputGuard):
    """ An input guard that always lets user input through.
    """

    def _detect(self, message_content: str) -> bool:
        return InputGuardFinding.OK
    