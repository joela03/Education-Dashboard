import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from functions import (get_credentials_from_env, enter_credentials_to_website, 
                       select_reports, filter_by_last_assessment, scrape_table,
                       convert_col_to_dt)

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        credential_list = get_credentials_from_env()
        enter_credentials_to_website(driver, credential_list)

        # Scrape enrolment reports
        select_reports(driver, 3)
        enrolment_df = scrape_table(driver, "gridStudentReport")

    finally:
        driver.quit()
    # filtered_df = convert_col_to_dt(df, ["Last\nProgress Check", "Last\nAssessment", "Last\nAttendance", "Last\nLP Update", "Last\nPR Sent"])
    # filtered_df = filter_by_last_assessment(df, "Progress Check", 28, False)
    