import os
from src.exceptions import AppException

def read_secret(env_variable: str, local_fallback: str = None) -> str:
    try:
        secret_path = os.getenv(env_variable)
        with open(secret_path, "r") as f:
            return f.read().strip()
    except Exception as e:  
        raise AppException(f"Failed to read secret: {e}")

OPENAI_API_KEY = read_secret("OPENAI_API_KEY", "./secrets/openai_api_key.txt")
LINKEDIN_ACCESS_TOKEN = read_secret("LINKEDIN_ACCESS_TOKEN", "./secrets/linkedin_access_token.txt")
