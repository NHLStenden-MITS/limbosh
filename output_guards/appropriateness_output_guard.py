import json
from llm.large_language_model import ChatMessage
from llm.large_language_model_factory import LargeLanguageModelFactory
from output_guards.output_guard import OutputGuard, OutputGuardFinding
from prompting.prompt_factory import PromptFactory


class AppropriatenessOutputGuard(OutputGuard):
    """ An output guard that assesses response appropriateness using a different LLM context to detect prompt injection.
    """

    def __init__(self, prompt_factory: PromptFactory, large_language_model_factory: LargeLanguageModelFactory):
        """ Initializes a new instance of an output guard that assesses response appropriateness using a different LLM context to detect prompt injection.
        
        Args:
            prompt_factory (PromptFactory): The prompt factory to use to generate the guard prompt.
            large_language_model_factory (LargeLanguageModelFactory): The LLM factory to use to acquire an LLM instance.
        """
        super().__init__()
        self.prompt_factory = prompt_factory
        self.large_language_model = large_language_model_factory.get()

    def _detect (self, input_message_content: str, output_message_content: str) -> OutputGuardFinding:
        # Render guard prompt.
        key_name = 'probable_deviation'
        guard_prompt = self.prompt_factory.get('appropriateness-output-guard', {
            'input': input_message_content,
            'output': output_message_content,
            'key_name': key_name,
        })

        # Pass to LLM.
        result = self.large_language_model.get_next_message([ChatMessage('user', guard_prompt)]).content

        # Parse output.
        try:
            parsed_result = json.loads(result)
        
            # The guard LLM is misbehaving. This should be treated as successful prompt injection so throw deviation.
            if key_name not in parsed_result or not parsed_result[key_name]:
                return OutputGuardFinding.PROBABLE_DEVIATION
        except json.JSONDecodeError:
            
            # Guard LLM did not produce valid JSON. Throw deviation.
            return OutputGuardFinding.PROBABLE_DEVIATION

        # Things look okay.
        return OutputGuardFinding.OK
