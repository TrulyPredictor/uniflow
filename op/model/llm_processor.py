"""LLM processor for processing data with a LLM model server."""
import copy
import json
from typing import Any, Dict, List

from uniflow.op.model.abs_llm_processor import AbsLLMProcessor
from uniflow.op.model.constants import ERROR, ERROR_CONTEXT, ERROR_LIST, RESPONSE
from uniflow.op.prompt import Context

OUTPUT_SCHEMA_GUIDE = "Ensure the response is in json."


class LLMDataProcessor(AbsLLMProcessor):
    """
    Data processor for processing data with a LLM model server.
    It handles serialization and deserialization of data,
    manages interactions with the LLM model server, and applies
    a guided prompt template to the data.
    """

    def _serialize(self, data: List[Context]) -> List[str]:
        """Serialize data.

        Args:
            data (List[Context]): Data to serialize.

        Returns:
            List[str]: Serialized data.
        """
        output = []
        for d in data:
            if not isinstance(d, Context):
                raise ValueError("Input data must be a Context object.")
            output_strings = []
            prompt_template = copy.deepcopy(self._prompt_template)
            if not prompt_template.instruction and not prompt_template.few_shot_prompt:
                for key, value in d.model_dump().items():
                    output_strings.append(f"{key}: {value}")
            else:
                prompt_template.few_shot_prompt.append(d)
                output_strings.append(f"instruction: {prompt_template.instruction}")
                for example in prompt_template.few_shot_prompt:
                    for ex_key, ex_value in example.model_dump().items():
                        output_strings.append(f"{ex_key}: {ex_value}")

            # Join all the strings into one large string, separated by new lines
            output_string = "\n".join(output_strings)
            output.append(output_string)
        return output

    def _deserialize(self, data: List[str]) -> List[Dict[str, Any]]:
        """Deserialize data.

        Args:
            data (List[str]): Data to deserialize.

        Returns:
            List[Dict[str, Any]]: Deserialized data.
        """
        return {
            RESPONSE: data,
            ERROR: "No errors.",
        }


class JsonFormattedDataProcessor(AbsLLMProcessor):
    """
    Extends the LLMDataProcessor Class to ensure the response is in json.
    """

    def _serialize(self, data: List[Context]) -> List[str]:
        """Serialize data.

        Args:
            data (List[Context]): Data to serialize.

        Returns:
            List[str]: Serialized data.
        """
        for d in data:
            if not isinstance(d, Context):
                raise ValueError("Input data must be a Context object.")
            prompt_template = copy.deepcopy(self._prompt_template)

            prompt_template.instruction = (
                f"{prompt_template.instruction}\n\n{OUTPUT_SCHEMA_GUIDE}"
            )

            input_data = []
            prompt_template.few_shot_prompt.append(d)
            input_data.append(prompt_template.model_dump())
        return [json.dumps(d) for d in input_data]

    def _deserialize(self, data: List[str]) -> List[Dict[str, Any]]:
        """Deserialize data.

        Args:
            data (List[str]): Data to deserialize.

        Returns:
            List[Dict[str, Any]]: Deserialized data.
        """
        error_count = 0
        output_list = []
        error_list = []
        error_context = []

        for d in data:
            try:
                output_list.append(json.loads(d))
            except json.JSONDecodeError as e:
                error_count += 1
                error_list.append(str(e))
                error_context.append(d)
                continue

        if error_count == 0:
            return {
                RESPONSE: output_list,
                ERROR: "No errors.",
            }
        return {
            RESPONSE: output_list,
            ERROR: f"Failed to deserialize {error_count} examples",
            ERROR_LIST: error_list,
            ERROR_CONTEXT: error_context,
        }
