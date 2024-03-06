from typing import Iterable, Literal
from urllib.request import urlopen

from openai import OpenAI

from llm.openai_large_language_model import OpenaiLargeLanguageModel
from .large_language_model import ChatMessage


class OllamaLargeLanguageModel(OpenaiLargeLanguageModel):
    """ Represents a large language model (LLM) hosted locally on Ollama.
    """

    def _get_api_url(self) -> str:
        """ Gets the URL of the local Ollama API.
    
        Returns:
            bool: The URL of the local Ollama API.
        """
        return f'http://localhost:{self.port}/v1'

    def _check_connectivity(self) -> bool:
        try:
            with urlopen(self._get_api_url()) as response:
                response.read() # Ensure local Ollama API is available.
                return True
        except:
            return False
    
    def __init__(self, port=11434, temperature=0.0001, model: Literal["llama2", "openchat", "gemma"] = "openchat"):
        """ Initializes a new instance of a large language model (LLM) hosted locally on Ollama.
        
        Args:
            temperature (float): The temperature to use for the LLM.
            model (str): The name of the model to query.
        """
        super(OllamaLargeLanguageModel, self).__init__(temperature)
        self.port = port
        self.api_key = "ollama"
        self.model = model
        self.client = OpenAI(base_url=self._get_api_url(), api_key=self.api_key)
        