import os
import pytest
from src.linkedin_service import linkedin_service

@pytest.mark.integration
def test_linkedin_integration_get_user_id():
    user_id = linkedin_service.get_user_id()
    assert user_id is not None
    assert isinstance(user_id, str)

@pytest.mark.integration
def test_linkedin_integration_real_call():
    user_id = linkedin_service.get_user_id()
    linkedin_service.post_to_linkedin("Hello World!", f"urn:li:person:{user_id}")
    
