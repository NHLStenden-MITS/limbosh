from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class InputGuardFinding(Enum):
    """ An enumeration of findings that input guards may make with regard to user input.
    """
    
    OK = 0
    """ Indicates that the input guard is allowing the input to proceed.
    """

    SPECIAL_COMMAND_CLEAR = 1
    """ Indicates that the input guard was provided with a console clear command.
    """

    SPECIAL_COMMAND_EXIT = 2
    """ Indicates that the input guard was provided with an exit command.
    """

    EMPTY_COMMAND = 3
    """ Indicates that the input guard was provided with an empty command.
    """

    PROBABLE_PROMPT_INJECTION = 4
    """ Indicates that the input guard has detected a probable prompt injection attack.
    """


class InputGuard(ABC):
    """ Represents an abstract input guard.
    """
    
    def __init__(self, next: Optional['InputGuard'] = None):
        """ Abstract constructor for an input guard.

        Args:
            next (Optional['InputGuard']): The next link in the input guard chain (if any).
        """
        self.next = next
        
    @abstractmethod
    def _detect (self, message_content: str) -> InputGuardFinding:
        """ Uses this input guard to check the given message.
        
        Override this method, rather than `detect`, in concrete implementations of this class.
        
        Args:
            message_content (str): The message content to check.
        Returns:
            InputGuardFinding: The finding of the input guard.
        """
        raise NotImplementedError("Cannot use an abstract input guard.")

    def detect (self, message_content: str) -> InputGuardFinding:
        """ Uses the input guard to check the given message.
        
        This method implementes a chain of responsibility pattern and should not be overridden. Override `_detect` instead.
        
        Args:
            message_content (str): The message content to check.
        Returns:
            InputGuardFinding: The finding of the input guard.
        """
        # Run own detect function.
        result = self._detect(message_content)
        if result != InputGuardFinding.OK:
            return result
        
        # Delegate to next link in chain-of-responsibility (if any).
        return InputGuardFinding.OK if self.next == None else self.next.detect(message_content)
    