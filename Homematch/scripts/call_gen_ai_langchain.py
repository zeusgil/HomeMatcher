import asyncio
import json
import os

from langchain.llms import OpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor

from scripts.models import HouseListing
from scripts.resources.consts import GPT4O_MODEL_NAME, EXTRA_SECURITY_GAP, MAX_OUTPUT_TOKENS_AMOUNT, \
    LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION, LISTINGS_FEW_SHOT_EXAMPLE


class GenAICaller:

    def __init__(self):
        self.executor = ThreadPoolExecutor()

    async def call_gen_ai(self, system_prompt: str,
                          prompt: str,
                          few_shot_examples: str = None,
                          parser: PydanticOutputParser = None) -> dict:
        gen_ai_response = await self._get_gen_ai_response(system_prompt, prompt, few_shot_examples, parser)
        gen_ai_response_jsonified = self._safe_json_loads(gen_ai_response)
        return gen_ai_response_jsonified

    async def _get_gen_ai_response(self, system_prompt, user_prompt: str,
                                   few_shot_examples: str = None,
                                   parser: PydanticOutputParser = None) -> str:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not system_prompt:
            print("WARNING: System prompt is empty")

        llm = OpenAI(model_name=GPT4O_MODEL_NAME, temperature=0.2,
                     max_tokens=MAX_OUTPUT_TOKENS_AMOUNT, api_key=openai_api_key)

        query = await self._create_query(few_shot_examples, parser, system_prompt, user_prompt)

        response = await asyncio.get_event_loop().run_in_executor(self.executor, llm.invoke,
                                                                  query)  # Async is not supported directly in LangChain
        response = self._correct_json_parsing(response)
        return response

    @staticmethod
    async def _create_query(few_shot_examples: str, parser: PydanticOutputParser,
                            system_prompt: str, user_prompt: str) -> str:
        prompt_template = """
        {system_prompt}
        {prompt}
        Examples:
        {few_shot_examples}
        """

        if parser is not None:
            prompt_template = """
            {system_prompt}
            {prompt}
            {format_instructions}
            Examples:
            {few_shot_examples}
            """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["system_prompt", "prompt", "few_shot_examples"],
            partial_variables={"format_instructions": parser.get_format_instructions()} if parser is not None else {}
        )
        query = prompt.format(
            system_prompt=system_prompt,
            prompt=user_prompt,
            few_shot_examples=few_shot_examples if few_shot_examples else ""
        )
        return query

    @staticmethod
    def _safe_json_loads(response: str) -> dict:
        try:
            return json.loads(response)

        except json.decoder.JSONDecodeError:
            print("Failed to decode JSON:", response)
            return {}

    @staticmethod
    def _correct_json_parsing(score: str) -> str:
        if "'''json" in score:
            score = score.split("'''json")[1].strip().replace("'''", "")
        elif "```json" in score:
            score = score.split("```json")[1].strip().replace("```", "")
        elif "'''" in score:
            score = score.split("'''")[1].strip().replace("'''", "")
        elif "```" in score:
            score = score.split("```")[1].strip().replace("```", "")
        return score


if __name__ == "__main__":
    gen_ai_caller = GenAICaller()
    gen_ai_response = asyncio.run(
        gen_ai_caller.call_gen_ai(LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION, LISTINGS_FEW_SHOT_EXAMPLE,
                                  parser=PydanticOutputParser(pydantic_object=HouseListing)))
    print(gen_ai_response)
