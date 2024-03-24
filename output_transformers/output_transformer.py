from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


class OutputTransformer(ABC):
    """ Represents an abstract output transformer.
    """
    
    def __init__(self, next: Optional['OutputTransformer'] = None):
        """ Abstract constructor for an output transformer.
        """
        self.next = next
        
    @abstractmethod
    def _transform (self, message_content: str) -> bool:
        """ Uses this output transformer to transform the given message.
        
        Override this method, rather than `transform`, in concrete implementations of this class.
        
        Args:
            message_content (str): The message content to transform.
        Returns:
            str: The transformed message.
        """
        raise NotImplementedError("Cannot use an abstract output transformer.")

    def transform (self, message_content: str) -> str:
        """ Uses this output transformer to transform the given message.
        
        This method implementes a chain of responsibility pattern and should not be overridden. Override `_transform` instead.
        
        Args:
            message_content (str): The message content to transform.
        Returns:
            str: The transformed message.
        """
        # Run own transformation function.
        transformed = self._transform(message_content)
        
        # Delegate to next link in chain-of-responsibility (if any).
        return self.next.transform(transformed) if self.next is not None else transformed
    