import openai
import logging
from config.config import Config

logger = logging.getLogger(__name__)
openai.api_key = Config.OPENAI_API_KEY
if not openai.api_key:
    logger.error("OpenAI API key is missing. Ensure OPENAI_API_KEY is set in environment variables.")


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
