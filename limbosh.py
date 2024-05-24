""" The honeypot shell that traps you in a conversation with an LLM pretending to be a shell.

Authors:
    Saul Johnson (saul.johnson@nhlstenden.com)
Since:
    28/02/2023
"""
import logging
import readline

from kink import di
from logstash_async.handler import AsynchronousLogstashHandler

from config.config_provider import ConfigProvider
from config.config_validator import ConfigValidator
from config.file_based_config_provider import FileBasedConfigProvider
from config.json_schema_config_validator import JsonSchemaConfigValidator
from input_guards.input_guard_factory import InputGuardFactory
from input_transformers.input_transformer_factory import InputTransformerFactory
from llm.built_in_context_compressor import BuiltInContextCompressor
from llm.context_compressor import ContextCompressor
from llm.large_language_model_factory import LargeLanguageModelFactory
from llm.passthrough_context_compressor import PassthroughContextCompressor
from output_guards.output_guard_factory import OutputGuardFactory
from output_transformers.output_transformer_factory import OutputTransformerFactory
from prompting.prompt_factory import PromptFactory
from shell.shell import Shell


# Initialize config file paths.
di['config_json_schema_file_path'] = './config.schema.json'
di['config_file_path'] = './config.json'

# Create application logger.
di[logging.Logger] = logging.getLogger(__name__)
# elk_logger = logging.getLogger('python-logstash-logger')
# elk_logger.setLevel(logging.DEBUG)
# elk_logger.addHandler(AsynchronousLogstashHandler('host.docker.internal', 50000, database_path=None))
# di[logging.Logger] = elk_logger

# Register all injected services.
di[ConfigValidator] = JsonSchemaConfigValidator()
di[ConfigProvider] = FileBasedConfigProvider()
di[ContextCompressor] = PassthroughContextCompressor()
di[InputTransformerFactory] = InputTransformerFactory()
di[InputGuardFactory] = InputGuardFactory()
di[LargeLanguageModelFactory] = LargeLanguageModelFactory()
di[OutputGuardFactory] = OutputGuardFactory()
di[OutputTransformerFactory] = OutputTransformerFactory()
di[PromptFactory] = PromptFactory()

# Initialize and run generative honeypot shell.
di[Shell].run()
