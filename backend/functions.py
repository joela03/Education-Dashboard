"""Functions that are used to interact with Mathnasium website"""
import os
import time
from datetime import datetime, timedelta
import ast

import pandas as pd
from pandas import isna
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from dotenv import load_dotenv


def get_credentials_from_env():
    """Get's username and password from .env fie"""

    # Loads credentials from secure env file
    load_dotenv()

    # Adds credentials to an array
    credential_list = [os.environ["MATHNASIUM_USERNAME"], os.environ["MATHNASIUM_PASSWORD"]]

    return credential_list

def sends_keys(driver, element_id: str, keys: str):
    """Finds element and sends given keys to """
    element = driver.find_element(By.ID, element_id)
    element.send_keys(keys)

def submit(driver, element_id:str):
    """Submit's submission"""
    element =  driver.find_element(By.ID, element_id)
    element.submit()

def enter_credentials_to_website(driver, credential_list):
    """Fills out username and password form"""

    # Directs to Student Monthly report page
    driver.get("https://radius.mathnasium.com/StudentReport")

    # Sends username and password to input
    sends_keys(driver, "UserName", credential_list[0])
    sends_keys(driver, "Password", credential_list[1])

    # Submits credentials
    submit(driver, "login")

def select_reports(driver, enrolmentdropdownvalue):
    """Download's report for last 4 weeks """

    # Select Enrolment option for the Enrolment dropdown
    interact_with_k_dropdown(driver, "enrollmentFiltersDropDownList", enrolmentdropdownvalue)

    # Extracts current date
    current_date = datetime.now()
    current_date_str = dt_to_string(current_date)

    # Subtracts 4 weeks from current date
    str_start_date = subtracted_date(current_date_str, 28)

    # Insert report start date and end date into date bar
    input_date(driver, current_date_str, "StudentReportEnd")
    input_date(driver, str_start_date, "StudentReportStart")

    # Selects items per page to be 1000
    select_report_count(driver, "gridStudentReport", 3)

    time.sleep(5)

def select_assessment_report(driver):
    """Selects correct filters for the assessment report"""

    driver.get("https://radius.mathnasium.com/AssessmentReport")

    interact_with_k_dropdown(driver, "groupedDropDownList", 2)
    select_dropdown_by_input(driver, 'enrollmentStatusMulti_taglist', "On Hold")
    select_dropdown_by_input(driver, "assessmentOptionMulti_taglist", "Mathnasium")
    
    for centre in ["Wimbledon UK", "Wimbledon@home (VC)"]:
        select_dropdown_by_input(driver, "AllCenterListMultiSelect_taglist", centre)

    # Extracts current date
    current_date = datetime.now()
    current_date_str = dt_to_string(current_date)

    # Subtracts 60 weeks from current date
    str_start_date = subtracted_date(current_date_str, 230)
    input_date(driver, str_start_date, 'ReportStart')

    checkbox = driver.find_element(By.ID, "noPostAssessmentCheck")
    checkbox.click()

    select_report_count(driver, "gridAssessmentReport", 3)

def select_enrolment_report(driver, enrolment_dropdown_value:int ):
    """Selects correct filters for the assessment report"""

    driver.get("https://radius.mathnasium.com/Enrollment/EnrollmentReport")

    for centre in ["Wimbledon UK", "Wimbledon@home (VC)"]:
        select_dropdown_by_input(driver, "AllCenterListMultiSelect_taglist", centre)

    interact_with_k_dropdown(driver, "EnrollmentStatusDropDown", enrolment_dropdown_value)

    select_report_count(driver, "gridEnrollmentReport", 3)

def select_hold_report(driver):
    """Selects reports for accounts on hold"""

    driver.get("https://radius.mathnasium.com/Holds/HoldsReport")
    current_date = datetime.now()
    current_date_str = dt_to_string(current_date)

    # Subtracts 4 weeks from current date
    str_start_date = subtracted_date(current_date_str, 183)
    input_date(driver, str_start_date, "ReportStart")
    select_report_count(driver, "gridHoldsReport", 3)

def subtracted_date(date, days: int):
    """Subtracts a given number of days from a date and returns date as a string"""

    # Converts date to datetime if not string
    if not isinstance(date, datetime):
        date = datetime.strptime(date, "%d/%m/%Y")

    # Subtracts given days from todays date and converts date object back to a string
    dt_subtracted_date = date - timedelta(days)
    str_subtracted_date = dt_subtracted_date.strftime("%d/%m/%Y")

    return str_subtracted_date

def click(driver, element_id):
    """"Click's JS element"""
    element =  driver.find_element(By.ID, element_id)
    element.click()

def dt_to_string(date) -> str:
    "Converts current date to a string in the dd/mm/yyyy format"

    str_date = date.strftime("%d/%m/%Y")

    return str_date

def interact_with_k_dropdown(driver, dropdown_id: str, dropdown_value: int):
    "Takes id of a dropdown and the value of the dropdown you want to select and selects it"

    time.sleep(3)
    # Interacts with elements using javascript
    js_script = f"""
    var dropdown = $("#{dropdown_id}").data("kendoDropDownList");
    dropdown.value('{dropdown_value}');
    dropdown.trigger("change");
    """

    driver.execute_script(js_script)
    time.sleep(1)

def input_date(driver, date: str, element_id: str):
    "Splits date by / and then joins array with an arrow key"

    #Splits date into an array
    split_reversed_date = date.split("/")

    # Sends date with Left Arrow key after every input
    element = driver.find_element(By.ID, element_id)

    element.send_keys(split_reversed_date[2], Keys.ARROW_LEFT,
                      split_reversed_date[1], Keys.ARROW_LEFT,
                      split_reversed_date[0])

def scrape_table(driver, table_id: str, progress_report: bool, enrolment_report: bool):
    """Scrapes content from the page and adds it to a pandas DataFrame."""

    time.sleep(5)

    # Find the table
    student_report_table = driver.find_element(By.ID, table_id)

    # Extract headers
    headers = [header.text.strip() for header in student_report_table.find_elements(By.TAG_NAME, 'th')]

    # Ensure headers exist and insert "Link" column after the first column
    if headers:
        headers.insert(1, headers[0] + " Link")  # First link column
        if enrolment_report:
            headers.append("Account Link")  # Append new column at the end if enrolment_report is true

    # Extract table rows
    rows = student_report_table.find_elements(By.TAG_NAME, 'tr')

    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')

        if cells:
            row_data = []
            
            # Extract text & link from the first column
            first_col_text = cells[0].text.strip()
            first_col_link = None

            link = cells[0].find_elements(By.TAG_NAME, 'a')
            if link:
                first_col_link = link[0].get_attribute("href")

            # Add first column text and link
            row_data.append(first_col_text)
            row_data.append(first_col_link)

            # Extract the progress report link (if applicable)
            if progress_report and len(cells) > 2:
                links_in_third_col = cells[2].find_elements(By.TAG_NAME, 'a')
                if len(links_in_third_col) > 1:
                    row_data[1] = links_in_third_col[1].get_attribute("href")  # Overwrite first link

            # Extract Account Name link (if enrolment report is enabled)
            account_name_link = None
            if enrolment_report and len(cells) > 3:
                links_in_account_col = cells[3].find_elements(By.TAG_NAME, 'a')
                if links_in_account_col:
                    account_name_link = links_in_account_col[0].get_attribute("href") 
                    
            # Append the remaining text columns (excluding first column)
            row_data.extend([cell.text.strip() for cell in cells[1:]])

            # If enrolment_report, append Account Name link
            if enrolment_report:
                row_data.append(account_name_link)

            # Ensure row length matches headers length
            while len(row_data) < len(headers):
                row_data.append(None)
            while len(row_data) > len(headers):
                row_data.pop()

            # Strip the entire row data to remove any stray whitespace that could cause empty rows
            row_data = [x.strip() if isinstance(x, str) else x for x in row_data]

            # Check if empty
            if not any(row_data):  
                continue

            data.append(row_data)

    # Handle missing headers (if table is empty)
    if not headers and data:
        headers = [f"Column {i+1}" for i in range(len(data[0]))]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Remove rows where all values are None or NaN
    df = df.dropna(how='all')

    return df

def convert_col_to_dt(df, columns: list):
    "Takes in list of columns and converts values to datetime objects"

    for i in columns:
        df[i] = df[i].replace("", None)
        df[i] = pd.to_datetime(df[i], format="%d/%m/%Y", errors='coerce')
        df[i] = df[i].where(pd.notna(df[i]), None)
        
    return df


def filter_by_last_assessment(df, assessment_type: str, date_period: int, asc: bool):
    "Filters the dataframe by last assessment in a given period of time"

    assessment_types = ["Progress Check", "Assessment"]

    if assessment_type not in assessment_types:
        return ValueError, "Invalid assessment type"

    # Sort df based on values
    sorted_df = df.sort_values(by=[f"Last\n{assessment_type}"], ascending=asc)


    # Filters df to have assessments in a given period of time only
    filtered_df = sorted_df.loc[sorted_df[f"Last\n{assessment_type}"] >
                                subtracted_date(datetime.now(), date_period)]
    print(filtered_df)

    return filtered_df.loc[:, ["Student First Name", "Student Last Name", "Year",
                            "Attendance", "Last\nAttendance", f"Last\n{assessment_type}"]]

def merge_df(df1, df2):
    "Merges df's horizontally"

    return pd.concat([df1, df2], ignore_index=True)

def select_report_count(driver, dropdown_id: str, index: int):
    "Selects the number of items displayed on your report"

    # Finds dropdown by the xpath
    dropdown = driver.find_element(By.XPATH,
                                   f'//*[@id="{dropdown_id}"]/div[1]/span[1]/span/select')
    driver.execute_script("arguments[0].style.display = 'block';", dropdown)

    # Classifies select object and selects the given index
    select = Select(dropdown)
    select.select_by_index(index)

def select_progress_report_batch(driver):
    "Navigate's to the progress report page"

    # Navigates to current progress report page
    driver.get("https://radius.mathnasium.com/ProgressReportManager/CurrentBatchDetail")
    time.sleep(15)

    # Selects the report to display 1000 items
    select_report_count(driver, "gridCurrentBatch", 3)
    time.sleep(3)

def add_mathnasium_id_column(df):
    
    if "Student Link" not in df.columns:
        print("'Student Link' column not found in DataFrame!")
        return df

    df["Mathnasium ID"] = df["Student Link"].apply(lambda x: x.split("/")[-1]
                                                   if pd.notna(x) else None)
    
    return df

def safe_date(value):
    """Converts NaT or NaN values to None"""
    return None if isna(value) else value

def percentage_to_float(string):
    """Converts a percentage string (e.g., '75%') to a float (e.g., 0.75)."""
    try:
        return float(string.strip().replace('%', ''))
    except ValueError:
        raise ValueError(f"Invalid percentage format: {string}")
    
def ensure_list(value):
    """Ensures the input is always a list"""
    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:
            evaluated_value = ast.literal_eval(value)
            if isinstance(evaluated_value, list):
                return evaluated_value
        except (ValueError, SyntaxError):
            return value.split(', ')

    return []

def select_dropdown_by_input(driver, input_id: str, target_value: str):
    """Enters a dropdown input."""
    
    # Identify input field
    input_xpath = f"//input[@aria-describedby='{input_id}']"
    input_field = driver.find_element(By.XPATH, input_xpath)
    
    input_field.click()
    input_field.clear()

    # Input the target value
    input_field.send_keys(target_value)
    time.sleep(1)

    # Simulate DOWN arrow key to navigate options
    input_field.send_keys(Keys.DOWN)
    time.sleep(0.5)

    # Simulate pressing ENTER to select the option
    input_field.send_keys(Keys.ENTER)
    
def check_for_popup(driver):
    """Checks if their is a pop up on the screen and closes it"""
    
    try:
        wait = WebDriverWait(driver, 10)
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close')]")))  
        close_button.click()

    except (TimeoutException, NoSuchElementException):
        print("Close button not found or div did not appear.")
        
        
def get_hold_dates(holds: str) -> datetime:
    """Takes a string with two dates and returns last date which when the hold ends"""
    try:
        if not holds or pd.isna(holds):
            return (None, None)
            
        # Extract only the first part before <br> if extra text is present
        date_part = holds.split('\n')[0].strip()

        # Ensure date range
        if " - " not in date_part:
            return (None, None)

        split_dates = date_part.split(" - ")
        hold_start_date = datetime.strptime(split_dates[0].strip(), "%d/%m/%y")
        hold_end_date = datetime.strptime(split_dates[-1].strip(), "%d/%m/%y")

        return (hold_start_date, hold_end_date)
    except (ValueError, IndexError, AttributeError):
        return (None, None)
    
def process_assessment_data(df, columns_to_drop=None):
    """Cleans the df"""
    clean_whitespace = lambda text: ' '.join(text.split())
    df.columns = [clean_whitespace(col) for col in df.columns]
    
    if 'Student First Name' in df.columns and 'Student Last Name' in df.columns:
        df['Student First Name'] = df.apply(lambda row: row['Student First Name'] + 
                                           ' ' + row['Student Last Name'], axis=1)
        
        # Rename columns
        df.rename(columns={"Student First Name": "Student", 
                          "Student First Name Link": "Student Link"}, inplace=True)
    
    # Drop specified columns if they exist
    if columns_to_drop:
        columns_to_drop = [col for col in columns_to_drop if col in df.columns]
        if columns_to_drop:
            df = df.drop(columns_to_drop, axis=1)
    
    return df

def setup_browser():
    """Sets up browser"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def wait_for_element(driver, locator, timeout=10):
    """Wait for element to be clickable with dynamic timeout"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        print(f"Element {locator} not found within {timeout} seconds")
        return None