import pytest
from unittest.mock import patch, MagicMock
from src.openai_service import openai_service
from src.exceptions import ServiceException

@patch("src.openai_service.openai_service.client")
@pytest.mark.unit
def test_openai_generate_post_success(mock_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Generated LinkedIn Post Content"
    mock_client.chat.completions.create.return_value = mock_response
    result = openai_service.generate_linkedin_post("Test Topic")
    assert result == "Generated LinkedIn Post Content"

@patch("src.openai_service.openai_service.client")
@pytest.mark.unit
def test_openai_generate_post_failure(mock_client):
    mock_client.chat.completions.create.side_effect = Exception("OpenAI API Down")
    with pytest.raises(ServiceException):
        openai_service.generate_linkedin_post("Test Topic")

