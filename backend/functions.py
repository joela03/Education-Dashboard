"""Functions that are used to interact with Mathnasium website"""
import os
import time
from datetime import datetime, timedelta

import pandas as pd

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from dotenv import load_dotenv


def get_credentials_from_env():
    """Get's username and password from .env fie"""

    # Loads credentials from secure env file
    load_dotenv()

    # Adds credentials to an array
    credential_list = [os.environ["MATHNASIUM_USERNAME"], os.environ["MATHNASIUM_PASSWORD"]]

    return credential_list

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
    # dropdown = driver.find_element(By.XPATH,
    #                                '//*[@id="gridStudentReport"]/div[1]/span[1]/span/select')
    # driver.execute_script("arguments[0].style.display = 'block';", dropdown)
    # select = Select(dropdown)
    # select.select_by_index(3)

    time.sleep(5)


def subtracted_date(date, days: int):
    """Subtracts a given number of days from a date and returns date as a string"""

    # Converts date to datetime if not string
    if not isinstance(date, datetime):
        date = datetime.strptime(date, "%d/%m/%Y")

    # Subtracts given days from todays date and converts date object back to a string
    dt_subtracted_date = date - timedelta(days)
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

def interact_with_k_dropdown(driver, dropdown_id: str, dropdown_value: int):
    "Takes id of a dropdown and the value of the dropdown you want to select and selects it"

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

def scrape_table(driver, table_id: str):
    "Scrapes content from the page and adds it to a pandas df"

    # Finds relevant table
    student_report_table = driver.find_element(By.ID, table_id)

    # Finds header row
    headers = [header.text for header in student_report_table.find_elements(By.TAG_NAME, 'th')]

    # Iterate through rows and extract data
    rows = student_report_table.find_elements(By.TAG_NAME, 'tr')

    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')

        if cells:
            row_data = [cell.text for cell in cells]
            data.append(row_data)

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df

def convert_col_to_dt(df, columns: list):
    "Takes in list of columns and converts values to datetime objects"

    for i in columns:
        df[i] = df[i].replace("", pd.NaT)
        df[i] = pd.to_datetime(df[i], format="%d/%m/%Y", errors='coerce')
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
    time.sleep(4)

    # Selects the report to display 1000 items
    select_report_count(driver, "gridCurrentBatch", 3)
    time.sleep(3)
