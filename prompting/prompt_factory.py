from jinja2 import Environment, PackageLoader, select_autoescape
from kink import inject

from config.config_provider import ConfigProvider

@inject
class PromptFactory():
    
    def __init__(self, config_provider: ConfigProvider):
        self.engine = Environment(
            loader=PackageLoader("limbosh"),
            autoescape=select_autoescape()
        )
        self.config = config_provider.get()


    def get(self, prompt_name: str):
        template = self.engine.get_template(f'{prompt_name}.jinja2')
        return template.render(**self.config.prompt)
