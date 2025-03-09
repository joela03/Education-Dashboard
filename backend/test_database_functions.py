import unittest
from unittest import mock
from imports import get_db_connection 

class TestGetDbConnection(unittest.TestCase):

    @mock.patch("psycopg2.connect")
    @mock.patch("os.getenv")
    def test_get_db_connection_success(self, mock_getenv, mock_connect):
        "Validates successful connection"
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
    def test_get_db_connection_missing_env_vars(self, mock_getenv):
        'Returns ValueError is returned if variable is not present'
        required_vars = ["DB_HOST", "DB_USER", "DB_NAME", "DB_PORT"]
        
        for var in required_vars:
            mock_getenv.side_effect = lambda key, var=var: (
                None if key == var else
                "5432" if key == "DB_PORT" else  # Return a valid port number as a string
                "test_value"  # Default value for other variables
            )

            # Check if ValueError is raised due to the missing environment variable
            with self.assertRaises(ValueError):
                get_db_connection()