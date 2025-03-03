import time
from functions import (get_credentials_from_env, enter_credentials_to_website, 
                       download_reports, filter_by_last_assessment, scrape_table,
                       convert_col_to_dt)

if __name__ == "__main__":
    credential_list = get_credentials_from_env()
    driver = enter_credentials_to_website(credential_list)
    driver = download_reports(driver)
    df = scrape_table(driver, "gridStudentReport")
    filtered_df = convert_col_to_dt(df, ["Last\nProgress Check", "Last\nAssessment", "Last\nAttendance", "Last\nLP Update", "Last\nPR Sent"])
    filtered_df = filter_by_last_assessment(df, "Progress Check", 28, False)
    