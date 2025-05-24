import os
import json
import pytest
from auth.authentication import AuthenticationManager

@pytest.fixture
def mock_client_id(tmp_path):
    """
    Create a temporary client ID file for testing.
    
    Returns:
        str: Path to temporary client ID file
    """
    client_id_data = {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "project_id": "test_project"
    }
    
    client_id_path = tmp_path / "client_id.json"
    with open(client_id_path, 'w') as f:
        json.dump(client_id_data, f)
    
    return str(client_id_path)

@pytest.fixture
def mock_credentials(tmp_path):
    """
    Create a temporary credentials file for testing.
    
    Returns:
        str: Path to temporary credentials file
    """
    credentials_data = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "token_expiry": "2024-01-01T00:00:00Z"
    }
    
    credentials_path = tmp_path / "credentials.json"
    with open(credentials_path, 'w') as f:
        json.dump(credentials_data, f)
    
    return str(credentials_path)

def test_load_client_id(mock_client_id):
    """
    Test loading of client ID configuration.
    """
    auth_manager = AuthenticationManager(client_id_path=mock_client_id)
    client_id_config = auth_manager.load_client_id()
    
    assert isinstance(client_id_config, dict)
    assert "client_id" in client_id_config
    assert "client_secret" in client_id_config

def test_load_credentials(mock_credentials):
    """
    Test loading of credentials.
    """
    auth_manager = AuthenticationManager(credentials_path=mock_credentials)
    credentials = auth_manager.load_credentials()
    
    assert isinstance(credentials, dict)
    assert "access_token" in credentials
    assert "refresh_token" in credentials

def test_validate_credentials(mock_credentials):
    """
    Test credentials validation.
    """
    auth_manager = AuthenticationManager()
    
    valid_credentials = {
        "access_token": "test_token",
        "refresh_token": "test_refresh",
        "token_expiry": "2024-01-01T00:00:00Z"
    }
    
    invalid_credentials_1 = {
        "access_token": "test_token"
    }
    
    invalid_credentials_2 = {}
    
    assert auth_manager.validate_credentials(valid_credentials) is True
    assert auth_manager.validate_credentials(invalid_credentials_1) is False
    assert auth_manager.validate_credentials(invalid_credentials_2) is False

def test_client_id_file_not_found():
    """
    Test handling of missing client ID file.
    """
    auth_manager = AuthenticationManager(client_id_path="non_existent_file.json")
    
    with pytest.raises(FileNotFoundError):
        auth_manager.load_client_id()

def test_credentials_file_not_found():
    """
    Test handling of missing credentials file.
    """
    auth_manager = AuthenticationManager(credentials_path="non_existent_file.json")
    
    assert auth_manager.load_credentials() is None