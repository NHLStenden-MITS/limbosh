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
        raise NotImplementedError("Cannot use an abstract context compressor.")

