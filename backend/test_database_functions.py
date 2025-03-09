import unittest
from unittest import mock
from unittest.mock import MagicMock
from imports import (get_db_connection, get_status_key)

class TestGetDbConnection(unittest.TestCase):

    @mock.patch("psycopg2.connect")
    @mock.patch("os.getenv")
    def test_get_db_connection_success(self, mock_getenv, mock_connect):
        """Validates successful connection"""
        mock_getenv.return_value = "test_value"

        mock_connect.return_value = "Mocked Connection Object"

        conn = get_db_connection()

        mock_connect.assert_called_once_with(
            host="test_value",
            user="test_value",
            dbname="test_value",
            port="test_value"
        )

        self.assertEqual(conn, "Mocked Connection Object")

    @mock.patch("os.getenv")
    @mock.patch("psycopg2.connect")
    def test_get_db_connection_missing_env_vars(self, mock_connect, mock_getenv):
        """Returns ValueError is returned if variable is not present"""
        required_vars = ["DB_HOST", "DB_USER", "DB_NAME", "DB_PORT"]
        
        for var in required_vars:
            mock_getenv.side_effect = lambda key, var=var: (
                None if key == var else
                "5432" if key == "DB_PORT" else
                "test_value"
            )

            # Check if ValueError is raised due to the missing environment variable
            with self.assertRaises(ValueError):
                get_db_connection()
    
    def test_get_status_key_enrolment(self):
        self.assertEqual(get_status_key("enrolment", "enrolled"), 0)
        self.assertEqual(get_status_key("enrolment", "on hold"), 1)
        self.assertIsNone(get_status_key("enrolment", "unknown"))

    def test_get_status_key_delivery(self):
        self.assertEqual(get_status_key("delivery", "in-centre"), 0)
        self.assertEqual(get_status_key("delivery", "@home"), 1)
        self.assertIsNone(get_status_key("delivery", "not existing"))

    def test_get_status_key_invalid_type(self):
        self.assertIsNone(get_status_key("invalid_type", "enrolled"))
        self.assertIsNone(get_status_key("unknown", "on hold"))

    def test_get_status_key_case_insensitivity(self):
        self.assertEqual(get_status_key("ENROLMENT", "ENROLLED"), 0)
        self.assertEqual(get_status_key("Delivery", "@HOME"), 1)
        self.assertEqual(get_status_key("DeLiVeRy", "In-Centre"), 0)