"Main scripts that webscrapes"

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from functions import (get_credentials_from_env, enter_credentials_to_website,
                       select_reports, scrape_table,convert_col_to_dt,
                       click, interact_with_k_dropdown, merge_df, select_progress_report_batch)

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        credential_list = get_credentials_from_env()
        enter_credentials_to_website(driver, credential_list)


        # # # Scrape enrolment reports
        # select_reports(driver, 3)
        # enrolment_df = scrape_table(driver, "gridStudentReport")

        # # Scrape hold reports
        # interact_with_k_dropdown(driver, "enrollmentFiltersDropDownList", 4)
        # click(driver, "btnsearch")
        # time.sleep(3)
        # hold_df = scrape_table(driver, "gridStudentReport")

        # # Combine both dataframes
        # joined_df = merge_df(enrolment_df, hold_df)

        # # Converting column with date values into date objects
        # joined_df = convert_col_to_dt(joined_df, ["Last\nProgress Check", "Last\nAssessment",
        #                                           "Last\nAttendance", "Last\nLP Update",
        #                                           "Last\nPR Sent"])
        # print(joined_df)

        # Scrapes progress reports
        select_progress_report_batch(driver)
        progress_df = scrape_table(driver, "gridCurrentBatch")
        print(progress_df)




    finally:
        driver.quit()
