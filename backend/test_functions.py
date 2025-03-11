import pytest
import pandas as pd
from datetime import datetime

import unittest
from unittest.mock import patch
from functions import (convert_col_to_dt, percentage_to_float, ensure_list)
from imports import get_status_key



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