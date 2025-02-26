"""Functions that are used to interact with Mathnasium website"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
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
    

def download_reports(driver):
    """Download's report for last 4 weeks """
    
    # Directs to Student Monthly report page
    driver.get("https://radius.mathnasium.com/StudentReport")
    
    # Select 3rd option of the dropdown Enrolment
    interact_with_k_dropdown(driver, "enrollmentFiltersDropDownList", 3, False)

    # Extracts current date
    current_date = datetime.now()
    current_date_str = dt_to_string(current_date)

    # # Subtracts 4 weeks from current date
    str_start_date = subtracted_date(current_date_str, 28)

    # # Insert report start date into date bar
    input_date(driver, current_date_str, "StudentReportEnd")
    input_date(driver, str_start_date, "StudentReportStart")
    
    # Selects to have 1000 elements on the page
    interact_with_k_dropdown(driver, "//*[@id='gridStudentReport']/div[1]/span[1]/span", 3, True)
    
    # Clicks search button
    click(driver, "btnsearch")
    time.sleep(15)
    
    return driver


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
    
def dt_to_string(date) -> str:
    "Converts current date to a string in the dd/mm/yyyy format"
    
    str_date = date.strftime("%d/%m/%Y")
    
    return str_date

def change_dropdown_value(path: str, value: str, driver):
    "Takes a given id and changes value of the dropdown to value variable"
    
    dropdown_element  = driver.find_element(By.XPATH, path)
    driver.execute_script(f"arguments[0].innerText = {value};", dropdown_element)

def interact_with_k_dropdown(driver, dropdown_id: str, dropdown_value: int, xpath: bool):
    "Takes id of a dropdown and the value of the dropdown you want to select and selects it"

    # If it is an xpath retreive the id of the element first
    if xpath:
        dropdown_element = driver.find_element(By.XPATH, dropdown_id)
        dropdown_id = dropdown_element.get_attribute("id")

    js_script = f"""
    var dropdown = $("#{dropdown_id}").data("kendoDropDownList");
    dropdown.value('{dropdown_value}');
    dropdown.trigger("change");
    """

    driver.execute_script(js_script)
    time.sleep(1)  # Give time for the UI to update

    # Verify selection
    selected_value = driver.execute_script(f"return $('#{dropdown_id}').data('kendoDropDownList').value();")
    print("Selected value:", selected_value)
    
def input_date(driver, date: str, element_id: str):
    "Splits date by / and then joins array with an arrow key"
    
    #Splits date into an array
    split_reversed_date = date.split("/")
    
    # Sends date with Left Arrow key after every input
    element = driver.find_element(By.ID, element_id)
    
    element.send_keys(split_reversed_date[2], Keys.ARROW_LEFT, split_reversed_date[1], Keys.ARROW_LEFT , split_reversed_date[0])
    