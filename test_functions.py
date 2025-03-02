import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from functions import convert_col_to_dt



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
