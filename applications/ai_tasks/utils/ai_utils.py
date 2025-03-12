import json
from typing import Type

import openai
import logging

from openai import OpenAI
from pydantic import BaseModel
from applications.ai_tasks.rq_rs.ai_rs import RephraseResponse
from config.config import Config

logger = logging.getLogger(__name__)
openai.api_key = Config.OPENAI_API_KEY

if not openai.api_key:
    logger.error("OpenAI API key is missing. Ensure OPENAI_API_KEY is set in environment variables.")


def call_open_ai_api(
    model: str, messages: list, temperature: float, n: int, frequency_penalty: int,
    user: str, validation_model: Type[BaseModel] = None
) -> str | Type[BaseModel]:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    if validation_model:
        response_format = json.dumps({k: v['type'] for k, v in validation_model.model_json_schema()['properties'].items()})
        messages[0]["content"] += f" Strictly output in JSON: {response_format}"

    max_retries = 3

    for attempt in range(max_retries):
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
                return validation_model.model_validate(json.loads(response))

            return response

        except Exception as e:
            logger.error(f"OpenAI API call failed (Retry {attempt + 1}/{max_retries}): {e}")

    return "API call failed after multiple attempts"


def rephrase_text(description: str) -> RephraseResponse:
    messages = [
        {"role": "system", "content": "You are an AI that rephrases text while preserving meaning."},
        {"role": "user", "content": f"Rephrase this: {description}"}
    ]

    rephrased_text = call_open_ai_api(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1,
        n=1,
        frequency_penalty=0,
        user="VHemanthC"
    )

    return RephraseResponse(original=description, rephrased=rephrased_text)