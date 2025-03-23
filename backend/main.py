"Main scripts that webscrapes"

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from functions import (get_credentials_from_env, enter_credentials_to_website,
                       select_reports, scrape_table,convert_col_to_dt,
                       click, interact_with_k_dropdown, merge_df,
                       select_progress_report_batch, add_mathnasium_id_column,
                       select_assessment_report, select_hold_report, select_enrolment_report)
from imports import (get_db_connection, import_students_to_database)

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        credential_list = get_credentials_from_env()
        enter_credentials_to_website(driver, credential_list)

        # Scrape student report
        select_reports(driver, 3)
        student_df = scrape_table(driver, "gridStudentReport", 0)

        # Scrape student who are on hold
        interact_with_k_dropdown(driver, "enrollmentFiltersDropDownList", 4)
        click(driver, "btnsearch")       
        student_hold_df = scrape_table(driver, "gridStudentReport", 0)
        
        # Scrape assessment report
        select_assessment_report(driver)
        assessments_df = scrape_table(driver, "gridAssessmentReport", 0)

        # Scrape enrolment reports
        select_enrolment_report(driver, 3)
        enrolment_df = scrape_table(driver, "gridEnrollmentReport", 0)

        select_enrolment_report(driver, 4)
        enrolment_hold_df = scrape_table(driver, "gridEnrollmentReport", 0)

        select_enrolment_report(driver, 2)
        pre_enrolment_df = scrape_table(driver, "gridEnrollmentReport", 0)
        
        # Merge enrolment reports
        hold_enrolment_df = merge_df(enrolment_df, enrolment_hold_df)
        joined_enrolment_df = merge_df(hold_enrolment_df, pre_enrolment_df)
        enrolment_df.to_csv('enrolment.csv', index=False) 

        # Scrape hold table
        select_hold_report(driver)
        hold_df = scrape_table(driver, "gridHoldsReport", 0)
        hold_df.to_csv('hold.csv', index=False) 

        # Combine both dataframes
        joined_df = merge_df(student_df, student_hold_df)

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

        # Create id column
        add_mathnasium_id_column(joined_df)

        # Scrapes progress reports
        select_progress_report_batch(driver)
        progress_df = scrape_table(driver, "gridCurrentBatch", 1)
        progress_df.rename(columns={"Student Link": "Account Link"}, inplace=True)

        # Merges the student report and progress report
        merged_df = pd.merge(joined_df,
                            progress_df[['Student', 'Total LP Skills Mastered',
                            'Total LP Skills', '% Skills\nMastered', "Account Link"]],
                            on=['Student'],
                            how='inner')

        # Removes irrelevant columns
        merged_df = merged_df.drop(['Student Last Name', 'Guardian Emails'
                                    ,'Virtual Center', ''], axis=1)

        # Cleans column names
        merged_df.columns = merged_df.columns.str.replace("\n", " ", regex=True)

        # Splits guardian string into seperate list items
        merged_df["Guardians"] = merged_df["Guardians"].str.split("\n")

    finally:
        driver.quit()

    conn = get_db_connection()
    import_students_to_database(conn, merged_df)
