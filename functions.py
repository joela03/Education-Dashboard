"""Functions that are used to interact with Mathnasium website"""

import os

def get_credentials_from_env():
    """Get's username and password from .env fie"""
    username = os.environ["USERNAME"]
    password = os.environ["password"]
    
    credential_list = [username, password]
    
    return credential_list
    
    