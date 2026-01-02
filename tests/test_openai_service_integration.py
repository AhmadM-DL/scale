import os
import pytest
from src.openai_service import openai_service

from logging import getLogger
logger = getLogger(__name__)

@pytest.mark.integration
def test_openai_integration_real_api():
    result = openai_service.generate_linkedin_post("Neural Networks")
    logger.info(result)
    assert isinstance(result, str)
    assert len(result) > 0
