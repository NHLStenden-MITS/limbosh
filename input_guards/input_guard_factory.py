from typing import Dict, Literal

from input_guards.chaining_input_guard import ChainingInputGuard
from input_guards.input_guard import InputGuard
from input_guards.passthrough_input_guard import PassthroughInputGuard


class InputGuardFactory():
    """ A static factory for creating input guard instances depending on application-level configuration.
    """

    @staticmethod
    def construct(input_guard_type: Literal['passthrough']) -> InputGuard:
        if input_guard_type == 'passthrough':
            return PassthroughInputGuard()
        raise NameError(f'Input guard "{input_guard_type}" unknown or not supported.')

    @classmethod
    def get(cls, configuration: Dict[str, str]):
        """ Returns a newly-constructed input guard instance based on the application configuration passed.

        Args:
            configuration (Dict[str, str]): The application configuration dictionary.
        Returns:
            InputGuard: The newly-constructed input guard.
        """
        config = configuration["input_guards"]
        if type(config) is str:
            return cls.construct(config)
        return ChainingInputGuard([cls.construct(input_guard) for input_guard in config])
