from typing import Callable, Iterable

from llm.context_compressor import ContextCompressor
from llm.large_language_model import ChatMessage


class PassthroughContextCompressor(ContextCompressor):
    """ Represents a context compressor that does not apply any context transformation.
    """
        
    def _compress (self, chat_messages: Iterable[ChatMessage], callback: Callable[[Iterable[ChatMessage]], None]):
        # Simply call back with same chat messages.
        callback(chat_messages)
