from output_guards.output_guard import OutputGuard, OutputGuardFinding


class PassthroughOutputGuard(OutputGuard):
    """ An output guard that always lets LLM output through.
    """

    def _detect(self, message_content: str) -> bool:
        return OutputGuardFinding.OK
    