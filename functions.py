"""Functions that are used to interact with Mathnasium website"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_credentials_from_env():
    """Get's username and password from .env fie"""
    username = os.environ["USERNAME"]
    password = os.environ["password"]
    
    credential_list = [username, password]
    
    return credential_list

def enter_credentials_to_website(credential_list: list):
    """Fills out username and password form"""
    driver = driver.get("http://www.google.com")
    
    element = driver.find_element(By.ID, "passwd-id")
    
    