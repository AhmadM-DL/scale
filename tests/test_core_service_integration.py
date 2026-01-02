import pytest
import os
from unittest.mock import patch, MagicMock
from src.core_service import core_service

@pytest.mark.integration
def test_core_service():
    core_service.post_to_linkedin()

