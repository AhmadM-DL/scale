import os
from src.exceptions import AppException

def read_secret(env_variable: str) -> str:
    try:
        secret_path = os.getenv(env_variable)
        with open(secret_path, "r") as f:
            return f.read().strip()
    except Exception as e:  
        raise AppException(f"Failed to read secret: {e}")