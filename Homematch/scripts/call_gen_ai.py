# import asyncio
# import json
# import os
# from typing import Union, List
#
# from openai import RateLimitError
# from openai import AsyncOpenAI
# from pydantic import BaseModel
# from scripts.resources.consts import GPT4O_MODEL_NAME, MAX_OUTPUT_TOKENS_AMOUNT, EXTRA_SECURITY_GAP, \
#     OPENAI_EMBEDDING_SMALL_MODEL_NAME, LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION
#
#
# class GenAICaller:
#     def __init__(self):
#         self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
#         self.semaphore = asyncio.Semaphore(4)
#
#     async def call_gen_ai(self, system_prompt, prompt: str) -> dict:
#         print("Calling GenAI...")
#         gen_ai_response = await self._get_gen_ai_response(system_prompt, prompt)
#         gen_ai_response_jsonified = self._safe_json_loads(gen_ai_response)
#         return gen_ai_response_jsonified
#
#     async def convert_to_embedding(self, text: Union[str, BaseModel]) -> List[float]:
#         print("Converting to embedding...")
#         if not text:
#             return []
#
#         async with self.semaphore:
#             response = await self.client.embeddings.create(input=text, model=OPENAI_EMBEDDING_SMALL_MODEL_NAME)
#             embedding = response.data[0].embedding
#             return embedding
#
#     async def _get_gen_ai_response(self, system_prompt, prompt: str) -> str:
#         if not prompt:
#             return ""
#
#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt},
#         ]
#
#         while True:
#             try:
#                 async with self.semaphore:
#                     response = await self.client.chat.completions.create(
#                         model=GPT4O_MODEL_NAME,
#                         messages=messages,
#                         temperature=0.2,
#                         max_tokens=MAX_OUTPUT_TOKENS_AMOUNT - EXTRA_SECURITY_GAP,
#                     )
#
#                 score = response.choices[0].message.content
#                 score = self._correct_json_parsing(score)
#                 print("Response received from GenAI")
#                 return score
#
#             except RateLimitError as e:
#                 print("Rate limit hit, waiting 5s before retrying...")
#                 await asyncio.sleep(5)
#
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 return ""
#
#     @staticmethod
#     def _correct_json_parsing(score: str) -> str:
#         if "'''json" in score:
#             score = score.split("'''json")[1].strip().replace("'''", "")
#         elif "```json" in score:
#             score = score.split("```json")[1].strip().replace("```", "")
#         elif "'''" in score:
#             score = score.split("'''")[1].strip().replace("'''", "")
#         elif "```" in score:
#             score = score.split("```")[1].strip().replace("```", "")
#         return score
#
#     @staticmethod
#     def _safe_json_loads(response: str) -> dict:
#         try:
#             return json.loads(response)
#
#         except json.decoder.JSONDecodeError:
#             print("Failed to decode JSON:", response)
#             return {}
#
#
# if __name__ == "__main__":
#     gen_ai_caller = GenAICaller()
#     gen_ai_response = asyncio.run(
#         gen_ai_caller.call_gen_ai(LISTINGS_SYSTEM_PROMPT, LISTINGS_PROMPT_QUESTION)
#     )
