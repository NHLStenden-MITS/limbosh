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
    def get_next_message (self, messsages: Iterable[ChatMessage]) -> ChatMessage:
        """ Sends a list of messages to an LLM and returns the next message suggested by the model.
        
        Args:
            messages (Iterable[ChatMessage]): Messages currently in context.
        Returns:
            ChatMessage: The LLM's response to the prompt.
        """
        raise NotImplementedError("Cannot query an abstract LLM.")
    