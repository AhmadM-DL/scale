import os
from openai import OpenAI
from src.config import OPENAI_API_KEY
from src.exceptions import ServiceException
from logging import getLogger
logger = getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def generate_linkedin_post(self, topic: str) -> str:        
        prompt = f"Write an engaging, professional LinkedIn post about the AI topic: '{topic}'."
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Failed to generate LinkedIn post: {e}")
            raise ServiceException(f"Failed to generate LinkedIn post: {e}")
    
    def _get_system_prompt(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        agent_path = os.path.join(base_dir, "agent.txt")
        with open(agent_path, "r", encoding="utf-8") as f:
            return f.read()

openai_service = OpenAIService(OPENAI_API_KEY)
        
