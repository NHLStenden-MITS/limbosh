import json
from typing import Callable, Iterable, List

from kink import inject

from llm.context_compressor import ContextCompressor
from llm.large_language_model import ChatMessage
from llm.large_language_model_factory import LargeLanguageModelFactory
from prompting.prompt_factory import PromptFactory


@inject
class BuiltInContextCompressor(ContextCompressor):
    """ Represents a context compressor that uses the configured LLM.
    """
    
    def __init__ (self, prompt_factory: PromptFactory, large_language_model_factory: LargeLanguageModelFactory):
        """ Initializes a new instance of a context compressor that uses the configured LLM.

        Args:
            prompt_factory (PromptFactory): The prompt factory to use to generate the system prompt.
            large_language_model_factory (LargeLanguageModelFactory): The LLM factory to use to generate an LLM instance.
        """
        self.prompt_factory = prompt_factory
        self.large_language_model = large_language_model_factory.get()
        
    def _compress (self, chat_messages: Iterable[ChatMessage], callback: Callable[[Iterable[ChatMessage]], None]):
        compression_prompt = self.prompt_factory.get('context-compressor', {
            'context': json.dumps([chat_message.to_dict() for chat_message in chat_messages])
        })

        # Pass to LLM.
        result = self.large_language_model.get_next_message([ChatMessage('user', compression_prompt)]).content
        
        # Parse raw compressed context.
        compressed_context_json = json.loads(result)
        compressed_chat_messages: List[ChatMessage] = []
        for compressed_chat_message_json in compressed_context_json:
            compressed_chat_messages.append(ChatMessage.from_dict(compressed_chat_message_json))
        print(compressed_chat_messages)

        # Invoke callback with compressed context.
        callback(compressed_chat_messages)
