import pytest
import pandas as pd
from datetime import datetime

import unittest
from unittest.mock import patch
from functions import convert_col_to_dt, percentage_to_float



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
        self.assertEqual(percentage_to_float("50%"), 0.5)
        self.assertEqual(percentage_to_float("100%"), 1.0)
        self.assertEqual(percentage_to_float("0%"), 0.0)
        self.assertEqual(percentage_to_float("75.5%"), 0.755)
    
    def test_spaces_and_formatting(self):
        self.assertEqual(percentage_to_float(" 50% "), 0.5)
        self.assertEqual(percentage_to_float("\t25%\n"), 0.25)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            percentage_to_float("50")
        with self.assertRaises(ValueError):
            percentage_to_float("abc%")
        with self.assertRaises(ValueError):
            percentage_to_float("%")
        with self.assertRaises(ValueError):
            percentage_to_float("") 