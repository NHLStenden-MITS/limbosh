from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Literal, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class OllamaConfig():
    """ Application configuration for connecting to an Ollama instance (useful for self-hosting LLMs).
    """
    
    hostname: str
    """ The hostname of the Ollama instance to connect to.
    """

    port: int
    """ The port to connect on.
    """


@dataclass_json
@dataclass
class Config():
    """ The application-level configuration object.
    """

    model_name: Literal[
        'gpt-3.5-turbo',
        'gpt-4',
        'openchat',
        'gemma',
        'mistral',
        'llama2',
        'tinyllama',
        'qwen',
        'mixtral'
    ]
    """ The name of the LLM to use.
    """
    
    openai_api_key: str
    """ The OpenAI API key to use to access GPT models.
    """
    
    shell: str
    """ The type of shell to mimic.
    """
    
    input_guards: List[Literal['passthrough', 'empty', 'exit', 'clear']]
    """ The input guards to use between the user and the LLM.
    """
    
    input_transformers: List[Literal['delimiting']]
    """ The input transformers to use between the user and the LLM.
    """
    
    output_transformers: List[Literal['stripping', 'line_breaking']]
    """ The output transformers to use between the LLM and the user.
    """
    
    prompt: Dict[str, str]
    """ Additional templating parameters to inject into prompt templates.
    """
    
    ollama: OllamaConfig
    """ Configuration for connecting to an Ollama instance (useful for self-hosting LLMs).
    """


class ConfigProvider(ABC):
    """ Represents a provider for application-level configuration.
    """

    @abstractmethod
    def get(self) -> Config:
        """ Gets the configuration object retrieved by this provider.

        Returns:
            Config: The configuration object retrieved by this provider.
        """
        raise NotImplementedError('You cannot use an abstract ConfigProvider.')
        