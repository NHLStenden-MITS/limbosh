from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Literal


@dataclass
class ChatMessage():
    """ Represents a chat message exchanged with an LLM.
    """
    
    role: Literal["user"] | Literal["system"]
    """ The role of the entity that added the message to the context.
    """
    
    content: str
    """ The content of the message.
    """


class LargeLanguageModel(ABC):
    """ Represents an abstract large language model.
    """
    
    def __init__(self, temperature=0.0001):
        """ Abstract constructor for a large language model.
        
        Args:
            temperature (float): The temperature to use for the LLM.
        """
        self.temperature = temperature
        
    @abstractmethod
    def _check_connectivity (self) -> bool:
        """ Checks whether connectivity to the LLM is present.

        Returns:
            bool: True if there is connectivity to the LLM, otherwise False.
        """
        raise NotImplementedError("Cannot check for connectivity to an abstract LLM.")
    
    @abstractmethod
    def _get_next_message (self, messages: Iterable[ChatMessage]) -> ChatMessage:
        """ Sends a list of messages to an LLM and returns the next message suggested by the model.

        Override this method, rather than `get_next_message`, in concrete implementations of this class.

        Args:
            messages (Iterable[ChatMessage]): Messages currently in context.
        Returns:
            ChatMessage: The LLM's response to the prompt.
        """
        raise NotImplementedError("Cannot query an abstract LLM.")

    def get_next_message (self, messages: Iterable[ChatMessage]) -> ChatMessage:
        """ Sends a list of messages to an LLM and returns the next message suggested by the model.
        
        This method implementes a connectivity check and should not be overridden. Override `_get_next_message` instead.

        Args:
            messages (Iterable[ChatMessage]): Messages currently in context.
        Returns:
            ChatMessage: The LLM's response to the prompt.
        """
        if self._check_connectivity():
            raise ConnectionError("Cannot connect to the LLM. Check your internet connection or ensure local service is running.")
        return self._get_next_message(messages)
    