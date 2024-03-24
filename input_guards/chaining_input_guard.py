from typing import List
from input_guards.passthrough_input_guard import PassthroughInputGuard
from input_guards.input_guard import InputGuard


class ChainingInputGuard(PassthroughInputGuard):
    """ An input guard that constructs a chain of responsibility from a list of input guards.
    """

    def __init__(self, chain: List[InputGuard]):
        """ Initializes a new instance of an input guard that constructs a chain of responsibility from a list of input guards.

        Args:
            chain (List[InputGuard]): The list of input guards to chain together.
        """
        super().__init__(None)

        # Construct chain.
        if len(chain) > 0:
            first_link = self
            latest_link = first_link
            for guard in chain:
                latest_link.next = guard
                latest_link = guard # Remember latest link.
