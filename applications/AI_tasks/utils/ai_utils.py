import openai
import logging
from config.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)
import openai

openai.api_key = "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"

def rephrase_text(description: str) -> str:

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that rephrases text while preserving meaning."},
                {"role": "user", "content": f"Rephrase this: {description}"}
            ],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {e}")
        return "Rephrasing failed. Try again later."
