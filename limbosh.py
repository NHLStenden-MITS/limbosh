""" The honeypot shell that traps you in a conversation with an LLM pretending to be a shell.

Authors:
    Saul Johnson (saul.johnson@nhlstenden.com)
Since:
    28/02/2023
"""
from kink import di
from logging import Logger, getLogger

from config.config_provider import ConfigProvider
from config.config_validator import ConfigValidator
from config.file_based_config_provider import FileBasedConfigProvider
from config.json_schema_config_validator import JsonSchemaConfigValidator
from input_guards.input_guard_factory import InputGuardFactory
from input_transformers.input_transformer_factory import InputTransformerFactory
from llm.large_language_model_factory import LargeLanguageModelFactory
from output_transformers.output_transformer_factory import OutputTransformerFactory
from prompting.prompt_factory import PromptFactory
from shell.shell import Shell


di['config_json_schema_file_path'] = './config.schema.json'
di['config_file_path'] = './config.json'

di[Logger] = getLogger(__name__)

di[ConfigValidator] = JsonSchemaConfigValidator()
di[ConfigProvider] = FileBasedConfigProvider()
di[InputTransformerFactory] = InputTransformerFactory()
di[InputGuardFactory] = InputGuardFactory()
di[LargeLanguageModelFactory] = LargeLanguageModelFactory()
di[OutputTransformerFactory] = OutputTransformerFactory()
di[PromptFactory] = PromptFactory()

di[Shell].run()
