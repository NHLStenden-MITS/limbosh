from abc import ABC, abstractmethod
import json
from typing import Iterable, List

from kink import inject

from llm.large_language_model import ChatMessage


@inject
class ContextCompressor(ABC):
    """ Represents an abstract context compressor.
    """

    @abstractmethod
    def compress (self, chat_messages: Iterable[ChatMessage]) -> Iterable[ChatMessage]:
        """ Compresses an LLM context.

        Args:
            chat_messages (Iterable[ChatMessage]): The chat messages to compress.
        Returns:
            Iterable[ChatMessage]: The compressed chat messages.
        """
        raise NotImplementedError("Cannot use an abstract context compressor.")

