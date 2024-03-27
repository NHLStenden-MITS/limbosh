import sys
from urllib.request import urlopen
from typing import Iterable, Literal

from openai import OpenAI
from .large_language_model import LargeLanguageModel, ChatMessage


class OpenaiLargeLanguageModel(LargeLanguageModel):
    """ Represents an OpenAI large language model (LLM).
    """
    
    def __init__(self, api_key: str, temperature=0, model: Literal["gpt-3.5-turbo", "gpt-4"] = "gpt-4"):
        """ Initializes a new instance of an OpenAI large language model (LLM).
        
        Args:
            api_key (str): The API key to use to query the model.
            temperature (float): The temperature to use for the LLM.
            model (str): The name of the model to query.
        """
        super(OpenaiLargeLanguageModel, self).__init__(temperature)
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
        
    def _check_connectivity(self) -> bool:
        try:
            with urlopen('https://api.openai.com/') as response:
                response.read() # Ensure OpenAI API is available.
                return True
        except:
            return False

    def _get_next_message (self, messsages: Iterable[ChatMessage]) -> ChatMessage:
        # Format messages for OpenAI API.
        messages = list(map(lambda message: {'role': message.role, 'content': message.content}, messsages))
        
        # Get response.
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages
        ).choices[0].message.content
        
        # Adapt and return.
        return ChatMessage('system', response)
    