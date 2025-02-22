"""Functions that are used to interact with Mathnasium website"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import os
import time
from dotenv import load_dotenv


def get_credentials_from_env():
    """Get's username and password from .env fie"""
    
    load_dotenv()
    
    credential_list = [os.environ["MATHNASIUM_USERNAME"], os.environ["MATHNASIUM_PASSWORD"]]
    
    return credential_list

def enter_credentials_to_website(credential_list: list):
    """Fills out username and password form"""
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://radius.mathnasium.com/Account/Login")
    
    sends_keys(driver, "UserName", credential_list[0])
    sends_keys(driver, "Password", credential_list[1])

    submit(driver, "login")
    
    try:
        bell = driver.find_element(By.ID, "bell")
        if bell:
            return driver
    except:
        driver.quit()
        raise ValueError("Incorrect Submission")
    
    
# def find_account_by_search(account_name: str, driver):
#     """Searches and directs to parent account on Radius"""
    
#     driver.get("https://radius.mathnasium.com/CustomerAccount")
    
#     search_bar = driver.find_element(By.ID, "AccountNameSearch")
#     search_bar.send_keys(account_name)
#     search_button = driver.find_element(By.ID, "btnsearch")
#     search_button.submit()
#     driver.findElement(By.linktext).get_attribute('href').click()
    
#     return driver

# def verify_valid_account_found(driver, account_name):
#     """Verifies that the right account was found"""
    
#     h2_element = driver.find_element(By.XPATH, "//h2[text()='Jen Waugh']")
#     h2_text = h2_element.text
    
#     if h2_text.strip() == account_name.strip():
#         return driver
#     else:
#         return NameError("Invalid account found.")
    

def download_reports(driver):
    """Download's report for last 4 weeks """
    
    # Directs to Student Monthly report page
    driver.get("https://radius.mathnasium.com/StudentReport")

    # Extracts current date
    end_date = extract_date(driver)

    # Subtracts 4 weeks from current date
    str_start_date = subtracted_date(end_date, 28)
    print(type(str_start_date))

    # Insert report start date into date bar
    sends_keys(driver, "ReportStart", str_start_date)

    # Clicks search button
    click(driver, "btnsearch")
    time.sleep(15)
    
    return driver

def extract_date(driver):
    """Extracts date and converts it to datetime"""
    time.sleep(3)
    
    date_input = driver.find_element(By.ID, "StudentReportEnd")
    date_value = date_input.get_attribute("value")

    # Converts string into datetime
    dt_date_value = datetime.strptime(date_value, "%d/%m/%Y")
    
    return dt_date_value

def subtracted_date(date, days: int):
    """Subtracts a given number of days from a date and returns date as a string"""

    # Converts date to datetime if not string
    if not isinstance(date, datetime):
        date = datetime.strptime(date, "%d/%m/%Y")

    dt_subtracted_date = date - timedelta(days=days)
    str_subtracted_date = dt_subtracted_date.strftime("%d/%m/%Y")

    return str_subtracted_date

def sends_keys(driver, element_id: str, keys: str):
    """Finds element and sends given keys to """
    element = driver.find_element(By.ID, element_id)
    element.send_keys(keys)

def submit(driver, element_id:str):
    """Submit's submission"""
    element =  driver.find_element(By.ID, element_id)
    element.submit()

def click(driver, element_id):
    """"Click's JS element"""
    element =  driver.find_element(By.ID, element_id)
    element.click()
    
def current_date() -> str:
    "Converts current date to a string in the dd/mm/yyyy format"
    
    date = datetime.now()
    str_date = date.strftime("%d/%m/%Y")
    
    return str_date