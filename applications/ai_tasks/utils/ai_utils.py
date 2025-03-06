import json
from typing import Type

import openai
import logging

from openai import OpenAI
from pydantic import BaseModel

from config.config import Config

logger = logging.getLogger(__name__)
openai.api_key = Config.OPENAI_API_KEY
if not openai.api_key:
    logger.error("OpenAI API key is missing. Ensure OPENAI_API_KEY is set in environment variables.")


def call_open_ai_api(model: str, messages: list, temperature: float, n: int, frequency_penalty: int,
                     user: str, validation_model: Type[BaseModel] = None) -> Type[BaseModel]:
    client = OpenAI(
        api_key=Config.OPENAI_API_KEY
    )
    openai.api_key = Config.OPENAI_API_KEY
    if validation_model:
        response_format = json.dumps({k: v['type'] for k, v in validation_model.schema()['properties'].items()})
        messages[0]["content"] += f"Give output Strictly in this JSON Format with no new-line characters: {response_format}"
    max_retries = 3
    response = None
    while max_retries > 0:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                n=n,
                frequency_penalty=frequency_penalty,
                user=user
            ).choices[0].message.content
            if validation_model:
                # print(f"Response before validation: {response}")
                response = validation_model.model_validate(json.loads(response))
                # print(f"After Validation {response=}")
                break
        except Exception as e:
            print((
                type(e).__name__,
                e,
                __file__,
                e.__traceback__.tb_lineno,
            ))

            max_retries -= 1
    return response


def rephrase_text(description: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that rephrases text while preserving meaning."},
                {"role": "user", "content": f"Rephrase this: {description}"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {e}")
        return "Rephrasing failed. Try again later."
