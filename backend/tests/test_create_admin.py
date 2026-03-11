import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Create a mock for backend.database and other dependencies before importing main
mock_db = MagicMock()
mock_models = MagicMock()
mock_auth = MagicMock()

sys.modules['backend.database'] = mock_db
sys.modules['backend.models'] = mock_models
sys.modules['backend.auth'] = mock_auth
sys.modules['sqlalchemy'] = MagicMock()
sys.modules['sqlalchemy.exc'] = MagicMock()
sys.modules['sqlalchemy.future'] = MagicMock()
sys.modules['sqlalchemy.ext.asyncio'] = MagicMock()
sys.modules['sqlalchemy.orm'] = MagicMock()
sys.modules['pydantic_settings'] = MagicMock()

# Now we can import main
from backend.scripts.create_admin import main

class TestCreateAdmin(unittest.TestCase):
    @patch('backend.scripts.create_admin.getpass.getpass')
    @patch('backend.scripts.create_admin.argparse.ArgumentParser.parse_args')
    @patch('backend.scripts.create_admin.create_admin', new_callable=AsyncMock)
    def test_main_success(self, mock_create_admin, mock_parse_args, mock_getpass):
        # Setup mocks
        mock_parse_args.return_value = MagicMock(username='testadmin')
        mock_getpass.return_value = 'securepassword'

        # Run main
        main()

        # Verify
        mock_getpass.assert_called_once_with("Admin password: ")
        mock_create_admin.assert_called_once_with('testadmin', 'securepassword')

    @patch('backend.scripts.create_admin.getpass.getpass')
    @patch('backend.scripts.create_admin.argparse.ArgumentParser.parse_args')
    @patch('backend.scripts.create_admin.create_admin', new_callable=AsyncMock)
    @patch('builtins.print')
    def test_main_empty_password(self, mock_print, mock_create_admin, mock_parse_args, mock_getpass):
        # Setup mocks
        mock_parse_args.return_value = MagicMock(username='testadmin')
        mock_getpass.return_value = ''

        # Run main
        main()

        # Verify
        mock_getpass.assert_called_once_with("Admin password: ")
        mock_create_admin.assert_not_called()
        mock_print.assert_called_once_with("Password cannot be empty.")

if __name__ == '__main__':
    unittest.main()
