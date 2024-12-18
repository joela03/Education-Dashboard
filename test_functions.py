import os
import pytest
import unittest
from unittest.mock import patch

from functions import get_credentials_from_env

class TestGetCredentialsFromEnv(unittest.TestCase):
    @patch.dict(os.environ, {"USERNAME": "test_user", "password": "test_pass"})
    def test_get_credentials_from_env(self):
        # Call the function
        credentials = get_credentials_from_env()

        # Assert the result
        self.assertEqual(credentials, ["test_user", "test_pass"])
