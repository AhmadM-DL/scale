import os, random, schedule, time
from src.openai_service import openai_service
from src.linkedin_service import linkedin_service
from src.exceptions import ServiceException

from logging import getLogger
logger = getLogger(__name__)

class CoreService:
    def __init__(self):
        pass

    def post_to_linkedin(self):
        try:
            topic= self._get_random_topic("src/topics.txt")
            post_content = openai_service.generate_linkedin_post(topic)
            counter = self._get_and_update_counter("src/counter.txt")
            post_content = f"AI/ML Digest #{counter} \n" + post_content 
            user_id = linkedin_service.get_user_id()
            linkedin_service.post_to_linkedin(post_content, f"urn:li:person:{user_id}")
        except Exception as e:
            logger.error(f"Unexpected error in job execution: {e}")
            raise ServiceException(f"Unexpected error in job execution: {e}")
    
    def _get_random_topic(self, file_path):
        if not os.path.exists(file_path):
            logger.error(f"Topics file not found at {file_path}")
            raise ServiceException(f"Topics file not found at {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]
        if not topics:
            logger.error("No topics found in topics.txt")
            raise ServiceException("No topics found in topics.txt")
        return random.choice(topics)
    
    def _get_and_update_counter(self, file_path):
        if not os.path.exists(file_path):
            logger.error("Counter file not found")
            raise ServiceException("Counter file not found")
        with open(file_path, "r", encoding="utf-8") as f:
            counter = int(f.read())
        counter += 1
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(counter))
        return counter

core_service = CoreService()