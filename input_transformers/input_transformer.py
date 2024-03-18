from abc import ABC, abstractmethod
from typing import Optional


class InputTransformer(ABC):
    """ Represents an abstract input transformer.
    """
    
    def __init__(self, next: Optional['InputTransformer'] = None):
        """ Abstract constructor for an input transformer.
        """
        self.next = next
        
    @abstractmethod
    def _transform (self, message_content: str) -> bool:
        """ Uses this input transformer to transform the given message.
        
        Override this method, rather than `transform`, in concrete implementations of this class.
        
        Args:
            message_content (str): The message content to transform.
        Returns:
            str: The transformed message.
        """
        raise NotImplementedError("Cannot use an abstract input transformer.")

    def transform (self, message_content: str) -> bool:
        """ Uses this input transformer to transform the given message.
        
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
    