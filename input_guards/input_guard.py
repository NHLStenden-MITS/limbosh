from abc import ABC, abstractmethod
from typing import Optional


class InputGuard(ABC):
    """ Represents an abstract input guard.
    """
    
    def __init__(self, next: Optional['InputGuard']):
        """ Abstract constructor for an input guard.
        """
        self.next = next
        
    @abstractmethod
    def _detect (self, message_content: str) -> bool:
        """ Uses this input guard to check the given message for a prompt injection attack.
        
        Override this method, rather than `detect`, in concrete implementations of this class.
        
        Args:
            message_content (str): The message content to check.
        Returns:
            bool: True if the message content represents a probable prompt injection attack, otherwise false.
        """
        raise NotImplementedError("Cannot use an abstract input guard.")

    def detect (self, message_content: str) -> bool:
        """ Uses the input guard to check the given message for a prompt injection attack.
        
        This method implementes a chain of responsibility pattern and should not be overridden. Override `_detect` instead.
        
        Args:
            message_content (str): The message content to check.
        Returns:
            bool: True if the message content represents a probable prompt injection attack, otherwise false.
        """
        # Run own detect function.
        if self._detect(message_content):
            return True
        
        # Delegate to next link in chain-of-responsibility (if any).
        return False if self.next == None else self.next.detect(message_content)
    