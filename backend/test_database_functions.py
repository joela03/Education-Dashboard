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