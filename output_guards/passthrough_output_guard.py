from output_guards.output_guard import OutputGuard, OutputGuardFinding


class PassthroughOutputGuard(OutputGuard):
    """ An output guard that always lets LLM output through.
    """

    def _detect (self, input_message_content: str, output_message_content: str) -> OutputGuardFinding:
        return OutputGuardFinding.OK
    