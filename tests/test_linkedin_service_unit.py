import pytest
from unittest.mock import patch, MagicMock
from src.linkedin_service import linkedin_service
from src.exceptions import ServiceException

@patch("requests.post")
@pytest.mark.unit
def test_linkedin_post_unit_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response
    
    linkedin_service.post_to_linkedin("Test content", "urn:li:person:123")
    mock_post.assert_called_once()

    _, kwargs = mock_post.call_args
    assert "Test content" in str(kwargs["json"])
    assert kwargs["json"]["author"] == "urn:li:person:123"

@patch("requests.post")
@pytest.mark.unit
def test_linkedin_post_unit_failure(mock_post):
    mock_post.side_effect = Exception("Network Error")
    with pytest.raises(ServiceException):
        linkedin_service.post_to_linkedin("Test content", "urn:li:person:123")

@patch("requests.get")
@pytest.mark.unit
def test_get_user_id_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"sub": "123"}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response
    
    result = linkedin_service.get_user_id()
    assert result == "123"
    mock_get.assert_called_once()

@patch("requests.get")
@pytest.mark.unit
def test_get_user_id_failure(mock_get):
    mock_get.side_effect = Exception("Failed")
    with pytest.raises(ServiceException):
        linkedin_service.get_user_id()
