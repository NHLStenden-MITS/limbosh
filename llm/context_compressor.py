from abc import ABC, abstractmethod
import json
import threading
from typing import Callable, Iterable, List

from kink import inject

from llm.large_language_model import ChatMessage


@inject
class ContextCompressor(ABC):
    """ Represents an abstract context compressor.
    """

    @abstractmethod
    def _compress (self, chat_messages: Iterable[ChatMessage], callback: Callable[[Iterable[ChatMessage]], None]):
        """ Compresses an LLM context.

        Override this method, rather than `compress`, in concrete implementations of this class.
        
        Args:
            chat_messages (Iterable[ChatMessage]): The chat messages to compress.
            callback (Callable[[Iterable[ChatMessage]]): The callback to invoke when context compression is finished.
        Returns:
            Iterable[ChatMessage]: The compressed chat messages.
        """
        raise NotImplementedError("Cannot use an abstract context compressor.")

    def compress (self, chat_messages: Iterable[ChatMessage], callback: Callable[[Iterable[ChatMessage]], None]):
        """ Compresses an LLM context.

        This method implementes threading and should not be overridden. Override `_compress` instead.
        
        Args:
            chat_messages (Iterable[ChatMessage]): The chat messages to compress.
            callback (Callable[[Iterable[ChatMessage]]): The callback to invoke when context compression is finished.
        Returns:
            Iterable[ChatMessage]: The compressed chat messages.
        """
        self.thread = threading.Thread(target=self._compress, args=[chat_messages, callback])
        self.thread.start()
