from typing import Dict

from llm.ollama_large_language_model import OllamaLargeLanguageModel
from llm.openai_large_language_model import OpenaiLargeLanguageModel


class LargeLanguageModelFactory():
    """ A static factory for creating large language model (LLM) instances depending on application-level configuration.
    """

    @staticmethod
    def get(configuration: Dict[str, str]):
        """ Returns a newly-constructed large language model (LLM) based on the application configuration passed.

        Args:
            configuration (Dict[str, str]): The application configuration dictionary.
        Returns:
            LargeLanguageModel: The newly-constructed LLM.
        """
        model_name = configuration['model_name']
        if model_name == 'openchat':
            return OllamaLargeLanguageModel(model='openchat')
        if model_name == 'gemma':
            return OllamaLargeLanguageModel(model='gemma')
        if model_name == 'llama2':
            return OllamaLargeLanguageModel(model='llama2')
        if model_name == 'gpt-3.5-turbo':
            return OpenaiLargeLanguageModel(model='gpt-3.5-turbo')
        if model_name == 'gpt-4':
            return OpenaiLargeLanguageModel(model='gpt-4')
        raise NameError(f'Model "{model_name}" unknown or not supported.')
