from abc import ABC, abstractmethod
import json
from typing import Iterable, List

from kink import inject

from llm.context_compressor import ContextCompressor
from llm.large_language_model import ChatMessage
from llm.large_language_model_factory import LargeLanguageModelFactory
from prompting.prompt_factory import PromptFactory


@inject
class BuiltInContextCompressor(ContextCompressor):
    
    def __init__(self, prompt_factory: PromptFactory, large_language_model_factory: LargeLanguageModelFactory):
        self.prompt_factory = prompt_factory
        self.large_language_model = large_language_model_factory.get()
        
    def compress (self, chat_messages: Iterable[ChatMessage]) -> Iterable[ChatMessage]:
        compression_prompt = self.prompt_factory.get('context-compressor', {
            'context': json.dumps([c.to_dict() for c in chat_messages])
        })

        # Pass to LLM.
        result = self.large_language_model.get_next_message([ChatMessage('user', compression_prompt)]).content
        print(result)
        
        jj = json.loads(result)
        cms: List[ChatMessage] = []
        for d in jj:
            cms.append(ChatMessage.from_dict(d))
        return cms
    