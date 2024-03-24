from typing import Dict

from kink import inject

from config.config_provider import ConfigProvider
from llm.ollama_large_language_model import OllamaLargeLanguageModel
from llm.openai_large_language_model import OpenaiLargeLanguageModel


@inject
class LargeLanguageModelFactory():
    """ A factory for creating large language model (LLM) instances depending on application-level configuration.
    """

    ollama_models = [
        'openchat',
        'gemma',
        'mistral',
        'llama2',
        'tinyllama',
        'qwen',
        'mixtral',
    ]
    """ The names of all Ollama models supported by the application.
    """

    openai_models = [
        'gpt-3.5-turbo',
        'gpt-4'
    ]
    """ The names of all OpenAI models supported by the application.
    """

    def __init__(self, config_provider: ConfigProvider):
        """ Initializes a new instance of a factory for creating large language model (LLM) instances depending on application-level configuration.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
        """
        self.config = config_provider.get()
    
    def get(self):
        """ Returns a newly-constructed large language model (LLM) based on the application configuration passed.
        
        Returns:
            LargeLanguageModel: The newly-constructed LLM.
        """
        if self.config.model_name in LargeLanguageModelFactory.ollama_models:
            return OllamaLargeLanguageModel(
                hostname=self.config.ollama.hostname, 
                port=self.config.ollama.port, 
                model=self.config.model_name)
        if self.config.model_name in LargeLanguageModelFactory.openai_models:
            return OpenaiLargeLanguageModel(
                api_key=self.config.openai_api_key, 
                model=self.config.model_name)
        raise NameError(f'Model "{self.config.model_name}" unknown or not supported.')
