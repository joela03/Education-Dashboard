"Main scripts that webscrapes"

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from functions import (get_credentials_from_env, enter_credentials_to_website,
                       select_reports, scrape_table,convert_col_to_dt,
                       click, interact_with_k_dropdown, merge_df,
                       select_progress_report_batch, add_mathnasium_id_column)

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        credential_list = get_credentials_from_env()
        enter_credentials_to_website(driver, credential_list)

        # Scrape enrolment reports
        select_reports(driver, 3)
        enrolment_df = scrape_table(driver, "gridStudentReport", "Student Report")

        # Scrape hold reports
        interact_with_k_dropdown(driver, "enrollmentFiltersDropDownList", 4)
        click(driver, "btnsearch")
        time.sleep(3)
        hold_df = scrape_table(driver, "gridStudentReport", "Student Report")

        # Combine both dataframes
        joined_df = merge_df(enrolment_df, hold_df)

        # Converting column with date values into date objects
        joined_df = convert_col_to_dt(joined_df, ["Last\nProgress Check", "Last\nAssessment",
                                                  "Last\nAttendance", "Last\nLP Update",
                                                  "Last\nPR Sent"])

        # Joins first name and last name of students
        joined_df['Student First Name'] = joined_df.apply(lambda row: row['Student First Name'] +
                                                        ' ' + row['Student Last Name'], axis=1)

        # Rename first column
        joined_df.rename(columns={"Student First Name": "Student",
                                "Student First Name Link": "Student Link" }, inplace=True)

        # Scrapes progress reports
        select_progress_report_batch(driver)
        progress_df = scrape_table(driver, "gridCurrentBatch", "Progress Report")

        # Create id column
        add_mathnasium_id_column(progress_df)

        # Merges the student report and progress report
        merged_df = pd.merge(joined_df,
                            progress_df[['Student', 'Total LP Skills Mastered',
                            'Total LP Skills', '% Skills\nMastered']],
                            on=['Student'],
                            how='inner')

        # Removes irrelevant columns
        merged_df = merged_df.drop(['Student Last Name', 'Guardian Emails'], axis=1)
        print(merged_df.columns.values)

    finally:
        driver.quit()
