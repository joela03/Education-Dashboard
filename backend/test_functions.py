import pytest
import pandas as pd
from datetime import datetime
import psycopg2
import unittest
from unittest.mock import MagicMock, patch
from functions import (convert_col_to_dt, percentage_to_float, ensure_list,
                       get_hold_dates)
from imports import get_status_key, get_student_id



def test_convert_col_to_dt():
    # Create a sample DataFrame
    data = {
        'date1': ['01/01/2024', '15/02/2023', '30/06/2022'],
        'date2': ['05/03/2021', '20/07/2020', '10/12/2019']
    }
    df = pd.DataFrame(data)
    
    # Convert columns to datetime
    df = convert_col_to_dt(df, ['date1', 'date2'])
    
    # Check if conversion was successful
    assert pd.api.types.is_datetime64_any_dtype(df['date1'])
    assert pd.api.types.is_datetime64_any_dtype(df['date2'])
    
    # Check if values are correctly parsed
    assert df.loc[0, 'date1'] == datetime(2024, 1, 1)
    assert df.loc[1, 'date2'] == datetime(2020, 7, 20)

def test_empty_string_handling():
    df =  pd.DataFrame({'date1': ['', '15/02/2023', '30/06/2022']})
    df = convert_col_to_dt(df, ['date1'])
    
    # Check if empty string is converted to NaT
    assert pd.isna(df.loc[0, 'date1'])
    assert df.loc[1, 'date1'] == datetime(2023, 2, 15)
    
class TestPercentageToFloat(unittest.TestCase):
    
    def test_valid_percentages(self):
        self.assertEqual(percentage_to_float("50%"), 50.0)
        self.assertEqual(percentage_to_float("100%"), 100.0)
        self.assertEqual(percentage_to_float("0%"), 0)
        self.assertEqual(percentage_to_float("75.5%"), 75.5)
    
    def test_spaces_and_formatting(self):
        self.assertEqual(percentage_to_float(" 50% "), 50.0)
        self.assertEqual(percentage_to_float("\t25%\n"), 25.0)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            percentage_to_float("abc%")
        with self.assertRaises(ValueError):
            percentage_to_float("%")
        with self.assertRaises(ValueError):
            percentage_to_float("")

def test_ensure_list():
    assert ensure_list(['Alice', 'Bob']) == ['Alice', 'Bob'], "Failed: Already a list"
    assert ensure_list("['Alice', 'Bob']") == ['Alice', 'Bob'], "Failed: Stringified list"
    assert ensure_list("Alice, Bob, Charlie") == ['Alice', 'Bob', 'Charlie'], "Failed: Comma-separated string"
    assert ensure_list("Alice") == ['Alice'], "Failed: Single string"
    assert ensure_list(None) == [], "Failed: None input"
    assert ensure_list(42) == [], "Failed: Integer input"
    assert ensure_list({'Alice': 'Bob'}) == [], "Failed: Dictionary input"
    assert ensure_list("[]") == [], "Failed: Empty stringified list"
    assert ensure_list("") == [""], "Failed: Empty string should return list with empty string"

def test_get_status_key():
    assert get_status_key("enrolment", "enrolment") == 0
    assert get_status_key("enrolment", "on hold") == 1
    assert get_status_key("delivery", "in-centre") == 0
    assert get_status_key("delivery", "@home") == 1
    
    assert get_status_key("Enrolment", "Enrolment") == 0
    assert get_status_key("ENROLMENT", "ON HOLD") == 1
    assert get_status_key("Delivery", "IN-CENTRE") == 0
    assert get_status_key("DELIVERY", "@HOME") == 1

    assert get_status_key("enrolment", "unknown") is None
    assert get_status_key("delivery", "office") is None
    assert get_status_key("random", "@home") is None
    assert get_status_key("", "") is None
    
    assert get_status_key(None, None) is None
    assert get_status_key(123, "enrolment") is None
    assert get_status_key("enrolment", 456) is None
    assert get_status_key([], {}) is None
    assert get_status_key("delivery", []) is None
    
class TestGetHoldDates(unittest.TestCase):
    def test_single_case(self):
        holds = """03/04/25 - 16/04/25
        All holds (2)"""
        expected = (datetime(2025, 4, 3), datetime(2025, 4, 16))
        self.assertEqual(get_hold_dates(holds), expected)

class TestGetStudentId(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock database connection for testing"""
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
    
    def test_valid_mathnasium_id(self):
        """Test with a valid mathnasium_id that exists in database"""
        # Setup mock return value
        expected_id = 123
        self.mock_cursor.fetchone.return_value = (expected_id,)
        
        # Call function
        result = get_student_id(self.mock_conn, 456)
        
        # Assertions
        self.assertEqual(result, expected_id)
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT student_id FROM student_information WHERE mathnasium_id = %s",
            (456,)
        )
    
    def test_nonexistent_mathnasium_id(self):
        """Test with a mathnasium_id that doesn't exist"""
        # Setup mock return value
        self.mock_cursor.fetchone.return_value = None
        
        # Call function
        result = get_student_id(self.mock_conn, 999)
        
        # Assertions
        self.assertIsNone(result)
    
    def test_null_mathnasium_id(self):
        """Test with None as mathnasium_id"""
        with self.assertRaises(psycopg2.Error):
            get_student_id(self.mock_conn, None)
    
    def test_database_error(self):
        """Test when database operation fails"""
        # Setup mock to raise exception
        self.mock_cursor.execute.side_effect = psycopg2.Error("DB error")
        
        # Call function
        result = get_student_id(self.mock_conn, 123)
        
        # Assertions
        self.assertIsNone(result)
        self.mock_conn.rollback.assert_called_once()
    
    def test_multiple_calls(self):
        """Test multiple consecutive calls"""
        # First call
        self.mock_cursor.fetchone.return_value = (111,)
        result1 = get_student_id(self.mock_conn, 456)
        self.assertEqual(result1, 111)
        
        # Second call
        self.mock_cursor.fetchone.return_value = None
        result2 = get_student_id(self.mock_conn, 789)
        self.assertIsNone(result2)
        

        self.assertEqual(self.mock_cursor.execute.call_count, 2)
