import os
import requests
from src.config import LINKEDIN_ACCESS_TOKEN
from src.exceptions import ServiceException
from logging import getLogger
logger = getLogger(__name__)

class LinkedInService:
    def __init__(self, access_token: str):
        self.access_token = access_token
    
    def get_user_id(self)->str:
        url = "https://api.linkedin.com/v2/userinfo"
        headers = {"Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            person_id = data.get("sub") or data.get("id")
            return person_id    
        except Exception as e:
            logger.error(f"Failed to get user ID: {e}")
            raise ServiceException(f"Failed to get user ID: {e}")
    
    def post_to_linkedin(self, content: str, user_id: str) -> bool:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202401",
            "Content-Type": "application/json",
        }
        post_data = {
            "author": user_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        try:
            response = requests.post(url, headers=headers, json=post_data)
            response.raise_for_status()
            return True
        except Exception as e:
            raise ServiceException(f"Failed to post to LinkedIn: {e}")

linkedin_service = LinkedInService(LINKEDIN_ACCESS_TOKEN)