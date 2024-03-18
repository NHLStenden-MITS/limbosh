from typing import Dict

from llm.ollama_large_language_model import OllamaLargeLanguageModel
from llm.openai_large_language_model import OpenaiLargeLanguageModel


class LargeLanguageModelFactory():
    """ A static factory for creating large language model (LLM) instances depending on application-level configuration.
    """

    ollama_models = [
        'openchat',
        'gemma',
        'mistral',
        'llama2',
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

    @classmethod
    def get(cls, configuration: Dict[str, str]):
        """ Returns a newly-constructed large language model (LLM) based on the application configuration passed.

        Args:
            configuration (Dict[str, str]): The application configuration dictionary.
        Returns:
            LargeLanguageModel: The newly-constructed LLM.
        """
        model_name = configuration['model_name']
        if model_name in cls.ollama_models:
            return OllamaLargeLanguageModel(
                hostname=configuration['ollama']['hostname'], 
                port=configuration['ollama']['port'],
                model=model_name)
        if model_name in cls.openai_models:
            return OpenaiLargeLanguageModel(
                api_key=configuration['openai_api_key'], 
                model=model_name)
        raise NameError(f'Model "{model_name}" unknown or not supported.')
