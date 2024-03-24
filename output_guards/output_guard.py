from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class OutputGuardFinding(Enum):
    """ An enumeration of findings that output guards may make with regard to LLM output.
    """
    
    OK = 0
    """ Indicates that the output guard is allowing the output to proceed.
    """

    PROBABLE_DEVIATION = 1
    """ Indicates that the output guard has discovered a probable deviation from the system prompt.
    """


class OutputGuard(ABC):
    """ Represents an abstract output guard.
    """
    
    def __init__(self, next: Optional['OutputGuard'] = None):
        """ Abstract constructor for an output guard.

        Args:
            next (Optional['OutputGuard']): The next link in the output guard chain (if any).
        """
        self.next = next
        
    @abstractmethod
    def _detect (self, message_content: str) -> OutputGuardFinding:
        """ Uses this output guard to check the given message.
        
        Override this method, rather than `detect`, in concrete implementations of this class.
        
        Args:
            message_content (str): The message content to check.
        Returns:
            OutputGuardFinding: The finding of the output guard.
        """
        raise NotImplementedError("Cannot use an abstract output guard.")

    def detect (self, message_content: str) -> OutputGuardFinding:
        """ Uses the output guard to check the given message.
        
        This method implementes a chain of responsibility pattern and should not be overridden. Override `_detect` instead.
        
        Args:
            message_content (str): The message content to check.
        Returns:
            OutputGuardFinding: The finding of the output guard.
        """
        # Run own detect function.
        result = self._detect(message_content)
        if result != OutputGuardFinding.OK:
            return result
        
        # Delegate to next link in chain-of-responsibility (if any).
        return OutputGuardFinding.OK if self.next == None else self.next.detect(message_content)
    