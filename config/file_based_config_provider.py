import json
from logging import Logger

from kink import inject
from config.config_provider import Config, ConfigProvider
from config.config_validator import ConfigValidator


@inject
class FileBasedConfigProvider(ConfigProvider):
    """ Represents a provider for application-level configuration that loads data from a local JSON file.
    """

    def __init__(self, config_file_path: str, config_validator: ConfigValidator, logger: Logger):
        """ Initialises a new instance of a provider for application-level configuration that loads data from a local JSON file.
        
        Args:
            config_file_path (str): The file from which to load the configuration.
            config_validator (ConfigValidator): The validator to use to validate the configuration.
            logger (Logger): The logger to use for this instance.
        """
        self.config_file_path = config_file_path
        self.config_validator = config_validator
        self.logger = logger

    def get(self) -> Config:
        # Load raw config from file.
        try:
            with open(self.config_file_path) as file:
                raw_config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.critical(f'Could not open config file at path: {self.config_file_path}')
            raise e

        # Validate the data, throwing an error on failure.
        valid, e = self.config_validator.validate(raw_config)
        if not valid:
            self.logger.critical(f'Application configuration was not valid.')
            raise e
        
        # Load into dataclass and return.
        return Config.from_json(json.dumps(raw_config))
