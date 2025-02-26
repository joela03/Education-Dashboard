import os
import pytest
import unittest
from unittest.mock import patch

from functions import get_credentials_from_env, current_date

def test_current_date():
    assert current_date() == "22/02/2025"
    
def test_current_date_type():
    assert type(current_date()) == str
    

