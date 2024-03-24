from typing import Literal

from kink import inject

from config.config_provider import ConfigProvider
from output_guards.chaining_output_guard import ChainingOutputGuard
from output_guards.output_guard import OutputGuard
from output_guards.passthrough_output_guard import PassthroughOutputGuard


@inject
class OutputGuardFactory():
    """ A factory for creating output guard instances depending on application-level configuration.
    """

    def __init__(self, config_provider: ConfigProvider):
        """ Initializes a new instance of a factory for creating output guard instances depending on application-level configuration.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
        """
        self.config = config_provider.get()

    @staticmethod
    def construct(output_guard_type: Literal['passthrough']) -> OutputGuard:
        """ Constructs an output guard based on its type token.

        Args:
            output_guard_type (Literal['passthrough']): The type token of the desired output guard.
        Returns:
            OutputGuard: An instance of the desired output guard.
        """
        if output_guard_type == 'passthrough':
            return PassthroughOutputGuard()
        raise NameError(f'Output guard "{output_guard_type}" unknown or not supported.')

    def get(self):
        """ Returns a newly-constructed output guard instance based on application-level configuration.

        Returns:
            OutputGuard: The newly-constructed output guard.
        """
        return ChainingOutputGuard([OutputGuardFactory.construct(output_guard) for output_guard in self.config.output_guards])
