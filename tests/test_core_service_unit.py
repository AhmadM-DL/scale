import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.core_service import core_service
from src.exceptions import ServiceException

@patch("src.core_service.openai_service")
@patch("src.core_service.linkedin_service")
def test_post_to_linkedin_success(mock_linkedin, mock_openai):
    # Mocking internal helper methods to isolate post_to_linkedin logic
    with patch.object(core_service, '_get_random_topic', return_value="Topic 1"), \
         patch.object(core_service, '_get_and_update_counter', return_value=5):
        
        mock_openai.generate_linkedin_post.return_value = "Post content"
        mock_linkedin.get_user_id.return_value = "123"
        
        core_service.post_to_linkedin()
        
        mock_openai.generate_linkedin_post.assert_called_once_with("Topic 1")
        mock_linkedin.get_user_id.assert_called_once()
        expected_content = "AI/ML Digest #5 \nPost content"
        mock_linkedin.post_to_linkedin.assert_called_once_with(expected_content, "urn:li:person:123")

@patch("os.path.exists")
def test_get_random_topic_file_not_found(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(ServiceException, match="Topics file not found"):
        core_service._get_random_topic("fake_path")

@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="Topic 1\nTopic 2")
def test_get_random_topic_success(mock_file, mock_exists):
    mock_exists.return_value = True
    topic = core_service._get_random_topic("fake_path")
    assert topic in ["Topic 1", "Topic 2"]

@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_get_random_topic_empty_file(mock_file, mock_exists):
    mock_exists.return_value = True
    with pytest.raises(ServiceException, match="No topics found"):
        core_service._get_random_topic("fake_path")

@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="10")
def test_get_and_update_counter_success(mock_file, mock_exists):
    mock_exists.return_value = True
    
    counter = core_service._get_and_update_counter("fake_counter.txt")
    
    assert counter == 11
    # Check that it was read then written
    mock_file.assert_any_call("fake_counter.txt", "r", encoding="utf-8")
    mock_file.assert_any_call("fake_counter.txt", "w", encoding="utf-8")
    mock_file().write.assert_called_once_with("11")

@patch("os.path.exists")
def test_get_and_update_counter_file_not_found(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(ServiceException, match="Counter file not found"):
        core_service._get_and_update_counter("fake_counter.txt")

@patch("src.core_service.openai_service")
def test_post_to_linkedin_failure(mock_openai):
    with patch.object(core_service, '_get_random_topic', return_value="Topic"), \
         patch.object(core_service, '_get_and_update_counter', return_value=1):
        mock_openai.generate_linkedin_post.side_effect = Exception("API Error")
        with pytest.raises(ServiceException, match="Unexpected error"):
            core_service.post_to_linkedin()
