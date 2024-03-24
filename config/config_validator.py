from abc import ABC, abstractmethod
from typing import Any


class ConfigValidator(ABC):
    """ Represents a validator for application-level configuration.
    """

    @abstractmethod
    def validate(self, data: Any) -> tuple[bool, Exception | None]:
        """ Uses this validator to validate the given configuration.

        Args:
            data (Any): The configuration object to validate.
        Returns:
            tuple[bool, Exception | None]: A tuple containing success status of validation and validation error (if any).
        """
        raise NotImplementedError('You cannot use an abstract ConfigValidator.')
