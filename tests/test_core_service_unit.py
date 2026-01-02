import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.core_service import core_service
from src.exceptions import ServiceException

@patch("src.core_service.openai_service")
@patch("src.core_service.linkedin_service")
@patch("src.core_service.random.choice")
@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="Topic 1\nTopic 2")
def test_post_to_linkedin_success(mock_file, mock_exists, mock_choice, mock_linkedin, mock_openai):
    mock_exists.return_value = True
    mock_choice.return_value = "Topic 1"
    mock_openai.generate_linkedin_post.return_value = "Post content"
    mock_linkedin.get_user_id.return_value = "123"
    
    core_service.post_to_linkedin()
    
    mock_openai.generate_linkedin_post.assert_called_once_with("Topic 1")
    mock_linkedin.get_user_id.assert_called_once()
    mock_linkedin.post_to_linkedin.assert_called_once_with("Post content", f"urn:li:person:123")

@patch("os.path.exists")
def test_get_random_topic_file_not_found(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(ServiceException, match="Topics file not found"):
        core_service._get_random_topic("fake_path")

@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_get_random_topic_empty_file(mock_file, mock_exists):
    mock_exists.return_value = True
    with pytest.raises(ServiceException, match="No topics found"):
        core_service._get_random_topic("fake_path")

@patch("src.core_service.openai_service")
def test_post_to_linkedin_failure(mock_openai):
    with patch.object(core_service, '_get_random_topic', return_value="Topic"):
        mock_openai.generate_linkedin_post.side_effect = Exception("API Error")
        with pytest.raises(ServiceException, match="Unexpected error"):
            core_service.post_to_linkedin()
