from typing import Literal

from kink import inject

from config.config_provider import ConfigProvider
from input_guards.chaining_input_guard import ChainingInputGuard
from input_guards.clear_input_guard import ClearInputGuard
from input_guards.empty_input_guard import EmptyInputGuard
from input_guards.exit_input_guard import ExitInputGuard
from input_guards.input_guard import InputGuard
from input_guards.passthrough_input_guard import PassthroughInputGuard


@inject
class InputGuardFactory():
    """ A factory for creating input guard instances depending on application-level configuration.
    """

    def __init__(self, config_provider: ConfigProvider):
        """ Initializes a new instance of a factory for creating input guard instances depending on application-level configuration.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
        """
        self.config = config_provider.get()

    @staticmethod
    def construct(input_guard_type: Literal['passthrough', 'empty', 'clear', 'exit']) -> InputGuard:
        """ Constructs an input guard based on its type token.

        Args:
            input_guard_type (Literal['passthrough', 'empty', 'clear', 'exit']): The type token of the desired input guard.
        Returns:
            InputGuard: An instance of the desired input guard.
        """
        if input_guard_type == 'passthrough':
            return PassthroughInputGuard()
        if input_guard_type == 'empty':
            return EmptyInputGuard()
        if input_guard_type == 'clear':
            return ClearInputGuard()
        if input_guard_type == 'exit':
            return ExitInputGuard()
        raise NameError(f'Input guard "{input_guard_type}" unknown or not supported.')

    def get(self):
        """ Returns a newly-constructed input guard instance based on application-level configuration.

        Returns:
            InputGuard: The newly-constructed input guard.
        """
        return ChainingInputGuard([InputGuardFactory.construct(input_guard) for input_guard in self.config.input_guards])
