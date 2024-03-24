import json
from logging import Logger
import jsonschema
from typing import Any

from kink import inject

from config.config_validator import ConfigValidator


@inject
class JsonSchemaConfigValidator(ConfigValidator):
    """ Represents a validator for application-level configuration that validates against a JSON schema.
    """

    def __init__(self, config_json_schema_file_path: str, logger: Logger):
        """ Initialises a new instance of a validator for application-level configuration that validates against a JSON schema.
        
        Args:
            config_json_schema_file_path (str): The file from which to load the configuration schema.
            logger (Logger): The logger to use for this instance.
        """
        try:
            with open(config_json_schema_file_path) as file:
                schema_data = json.load(file)
            jsonschema.Validator.check_schema(schema_data) # Validate that schema itself is valid.
        except FileNotFoundError as e:
            logger.critical(f'Could not load JSON schema file at {config_json_schema_file_path} to validate configuration.')
            raise e
        except (json.JSONDecodeError, jsonschema.SchemaError) as e:
            logger.critical(f'JSON schema file at {config_json_schema_file_path} is invalid and cannot be used to validate configuration.')
            raise e
        self.schema = schema_data

    def validate(self, data: Any) -> tuple[bool, Exception | None]:
        try:
            jsonschema.validate(data, self.schema)
            return (True, None) # Validation passed, all good!
        except Exception as e:
            return (False, e) # Validation failed.
        