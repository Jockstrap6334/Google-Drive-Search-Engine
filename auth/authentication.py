import json
from typing import Dict, Optional

class AuthenticationManager:
    """
    Manages authentication for Google Drive API access.
    Handles credential loading, validation, and token management.
    """
    def __init__(self, client_id_path: str = '.auth/client_id.json', 
                 credentials_path: str = '.auth/credentials.json'):
        """
        Initialize authentication manager with paths to credentials.
        
        Args:
            client_id_path (str): Path to client ID configuration
            credentials_path (str): Path to stored credentials
        """
        self.client_id_path = client_id_path
        self.credentials_path = credentials_path
    
    def load_client_id(self) -> Dict[str, str]:
        """
        Load client ID configuration from JSON file.
        
        Returns:
            Dict[str, str]: Client ID configuration
        
        Raises:
            FileNotFoundError: If client ID file is missing
            json.JSONDecodeError: If file is not valid JSON
        """
        try:
            with open(self.client_id_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Client ID file not found at {self.client_id_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in client ID file at {self.client_id_path}")
    
    def load_credentials(self) -> Optional[Dict[str, str]]:
        """
        Load stored credentials from JSON file.
        
        Returns:
            Optional[Dict[str, str]]: Loaded credentials or None if not found
        """
        try:
            with open(self.credentials_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in credentials file at {self.credentials_path}")
    
    def validate_credentials(self, credentials: Dict[str, str]) -> bool:
        """
        Validate the structure and basic requirements of credentials.
        
        Args:
            credentials (Dict[str, str]): Credentials to validate
        
        Returns:
            bool: Whether credentials are valid
        """
        required_keys = ['access_token', 'refresh_token', 'token_expiry']
        return all(key in credentials for key in required_keys)