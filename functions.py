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
    
def find_account_by_search(account_name: str, driver):
    """Searches and directs to parent account on Radius"""
    
    search_bar = driver.find_element(By.ID, "ContactSearch")
    search_bar.send_keys(account_name)
    search_button = driver.find_element(By.ID, "globalbtnsearch")
    search_button.submit()
    href = driver.find_element_by_css_selector("linker").get_attribute('href')
    driver.get(f"https://radius.mathnasium.com{href}")
    
    return driver

def verify_valid_account_found(driver, account_name):
    """Verifies that the right account was found"""
    
    h2_element = driver.find_element(By.XPATH, "//h2[text()='Jen Waugh']")
    h2_text = h2_element.text
    
    if h2_text.strip() == account_name.strip():
        return driver
    else:
        return NameError("Invalid account found.")
    
    
    