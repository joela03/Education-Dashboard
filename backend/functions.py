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

def scrape_table(driver, table_id: str, progress_report: bool):
    "Scrapes content from the page and adds it to a pandas df"

    time.sleep(3)

    # Find the table
    student_report_table = driver.find_element(By.ID, table_id)

    # Extract headers
    headers = [header.text.strip() for header in
            student_report_table.find_elements(By.TAG_NAME, 'th')]

    # Ensure headers are available
    if headers and len(headers) > 0:
        headers.insert(1, headers[0] + " Link")

    # Extract table rows
    rows = student_report_table.find_elements(By.TAG_NAME, 'tr')

    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')

        if cells:
            row_data = []
            first_col_text = cells[0].text.strip()
            first_col_link = None

            # Extract the link if present in the first column
            link = cells[0].find_elements(By.TAG_NAME, 'a')
            if link:
                first_col_link = link[0].get_attribute("href")

            # Append text and link
            row_data.append(first_col_text)
            row_data.append(first_col_link)

            # If progress_report, extract the second <a> tag
            if progress_report and len(cells) > 2:
                links_in_third_col = cells[2].find_elements(By.TAG_NAME, 'a')
                if len(links_in_third_col) > 1:
                    row_data[1] = links_in_third_col[1].get_attribute("href")

            # Append the remaining columns as text
            row_data.extend([cell.text.strip() for cell in cells[1:]])

            data.append(row_data)

    # Handle missing headers
    if not headers and data:
        headers = [f"Column {i+1}" for i in range(len(data[0]))]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df

def convert_col_to_dt(df, columns: list):
    "Takes in list of columns and converts values to datetime objects"

    for i in columns:
        df[i] = df[i].replace("", None)
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

def add_mathnasium_id_column(df):
    "Extracts id from link column and makes new Mathnasium ID column"

    df["Mathnasium ID"] = df["Student Link"].apply(lambda x: x.split("/")[-1]
                                                   if pd.notna(x) else None)

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