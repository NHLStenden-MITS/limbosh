from typing import List
from output_guards.passthrough_output_guard import PassthroughOutputGuard
from output_guards.output_guard import OutputGuard


class ChainingOutputGuard(PassthroughOutputGuard):
    """ An output guard that constructs a chain of responsibility from a list of output guards.
    """

    def __init__(self, chain: List[OutputGuard]):
        """ Initializes a new instance of an output guard that constructs a chain of responsibility from a list of output guards.

        Args:
            chain (List[OutputGuard]): The list of output guards to chain together.
        """
        super().__init__(None)

        # Construct chain.
        if len(chain) > 0:
            first_link = self
            latest_link = first_link
            for guard in chain:
                latest_link.next = guard
                latest_link = guard # Remember latest link.
