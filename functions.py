"""Functions that are used to interact with Mathnasium website"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv


def get_credentials_from_env():
    """Get's username and password from .env fie"""
    
    load_dotenv()
    
    username = os.environ["MATHNASIUM_USERNAME"]
    password = os.environ["MATHNASIUM_PASSWORD"]
    
    credential_list = [username, password]
    
    return credential_list

def enter_credentials_to_website(credential_list: list):
    """Fills out username and password form"""
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://radius.mathnasium.com/Account/Login")
    
    username_box = driver.find_element(By.ID, "UserName")
    username_box.send_keys(credential_list[0])
    password_box = driver.find_element(By.ID, "Password")
    password_box.send_keys(credential_list[1])
    submit_button =  driver.find_element(By.ID, "login")
    submit_button.submit()
    
    return driver
    
def check_successful_login(driver):
    """Check's that login is successful via url"""
    
    bell = driver.find_element(By.ID, "bell")
    if bell:
        return driver
    else:
        return ValueError("Incorrect Sumbmission")
    
    