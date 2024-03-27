from typing import Dict
from jinja2 import Environment, PackageLoader, select_autoescape
from kink import inject

from config.config_provider import ConfigProvider


@inject
class PromptFactory():
    """ A factory for generating prompts from template files.
    """

    def __init__(self, config_provider: ConfigProvider):
        """ Initializes a new instance of a factory for generating prompts from template files.

        Args:
            config_provider (ConfigProvider): The application-level configuration provider.
        """
        self.engine = Environment(
            loader=PackageLoader('limbosh'),
            autoescape=select_autoescape()
        ) # Initialize Jinja2 environment.
        self.config = config_provider.get()

    def get(self, prompt_name: str, extra_params: Dict[str, str] = {}):
        """ Gets the prompt with the specified name.

        Args:
            prompt_name (str): The name of the prompt to get (the filename of the template without extension).
            extra_params (Dict[str, str]): Any additional templating parameters to include when rendering the prompt.
        Returns:
            str: The rendered prompt.
        """
        template = self.engine.get_template(f'{prompt_name}.jinja2')
        return template.render(**self.config.prompt, **extra_params)
