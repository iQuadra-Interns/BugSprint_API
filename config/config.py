import os
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HASHING_SALT_ROUNDS = 12
