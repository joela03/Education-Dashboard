import pandas as pd
import json
from functions import (get_credentials_from_env, enter_credentials_to_website,
                       select_reports, scrape_table, convert_col_to_dt,
                       click, interact_with_k_dropdown, merge_df,
                       select_progress_report_batch, add_mathnasium_id_column,
                       select_assessment_report, select_hold_report, select_enrolment_report,
                       check_for_popup, get_hold_dates, setup_browser)

from imports import (get_db_connection, import_students_to_database, insert_into_assessments_db,
                    insert_into_enrolments_db, insert_into_holds_db, insert_preenroled_into_students)

def lambda_handler(event, context):
    try:
        driver = setup_browser()

        try:
            credential_list = get_credentials_from_env()
            enter_credentials_to_website(driver, credential_list)
            
            check_for_popup(driver)

            # Scrape student report
            select_reports(driver, 3)
            student_df = scrape_table(driver, "gridStudentReport", 0, 0)

            # Scrape student who are on hold
            interact_with_k_dropdown(driver, "enrollmentFiltersDropDownList", 4)
            click(driver, "btnsearch")       
            student_hold_df = scrape_table(driver, "gridStudentReport", 0, 0)
            
            # Scrape assessment report
            select_assessment_report(driver)
            assessments_df = scrape_table(driver, "gridAssessmentReport", 0, 0)
            clean_whitespace = lambda text: ' '.join(text.split())
            assessments_df.columns = [clean_whitespace(col) for col in assessments_df.columns]

            # Joins first name and last name of students
            assessments_df['Student First Name'] = assessments_df.apply(lambda row: row['Student First Name'] +
                                                            ' ' + row['Student Last Name'], axis=1)
            assessments_df.rename(columns={"Student First Name": "Student",
                            "Student First Name Link": "Student Link" }, inplace=True)

            # Drop useless columns
            assessments_df.rename(columns={"Student First Name": "Student",
                                    "Student First Name Link": "Student Link" }, inplace=True)
            assessments_df = assessments_df.drop(['Signup Date','Virtual Center'], axis=1)

            # Scrape enrolment reports
            select_enrolment_report(driver, 3)
            enrolment_df = scrape_table(driver, "gridEnrollmentReport", 0, 1)

            select_enrolment_report(driver, 4)
            enrolment_hold_df = scrape_table(driver, "gridEnrollmentReport", 0, 1)

            select_enrolment_report(driver, 2)
            pre_enrolment_df = scrape_table(driver, "gridEnrollmentReport", 0, 1)
            
            # Merge enrolment reports
            hold_enrolment_df = merge_df(enrolment_df, enrolment_hold_df)
            joined_enrolment_df = merge_df(hold_enrolment_df, pre_enrolment_df)
            joined_enrolment_df.columns = [col.replace("\n", " ").strip() for col in joined_enrolment_df.columns]

            joined_enrolment_df.rename(columns={"Student First Name": "Student",
                    "Student First Name Link": "Student Link"}, inplace=True)
            joined_enrolment_df = add_mathnasium_id_column(joined_enrolment_df)
            
            if not pre_enrolment_df.empty:
                pre_enrolment_df['Student First Name'] = pre_enrolment_df.apply(lambda row: row['Student First Name'] +
                                                ' ' + row['Student Last Name'], axis=1)
                pre_enrolment_df.rename(columns={"Student First Name": "Student",
                        "Student First Name Link": "Student Link"}, inplace=True)
                pre_enrolment_df.columns = [col.replace("\n", " ").strip() for col in pre_enrolment_df.columns]
                pre_enrolment_df.columns = pre_enrolment_df.columns.str.replace("\n", " ", regex=True)
                pre_enrolment_df = add_mathnasium_id_column(pre_enrolment_df)

            # Scrape hold table
            select_hold_report(driver)
            hold_df = scrape_table(driver, "gridHoldsReport", 0, 0)
            hold_df.columns = [col.replace("\n", " ").strip() for col in hold_df.columns]
            hold_df[['Hold start date', 'Hold end date']] = pd.DataFrame(hold_df['Holds'].apply(get_hold_dates).to_list(), index=hold_df.index)

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
            progress_df = scrape_table(driver, "gridCurrentBatch", 1, 0)
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

        insert_preenroled_into_students(conn, pre_enrolment_df)

        insert_into_assessments_db(conn, assessments_df)

        insert_into_enrolments_db(conn, joined_enrolment_df)

        insert_into_holds_db(conn, hold_df)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data scraping and database update completed successfully',
                'student_count': len(merged_df),
                'assessment_count': len(assessments_df),
                'enrollment_count': len(joined_enrolment_df),
                'hold_count': len(hold_df)
            })
        }
        
    except Exception as e:
        print(f"Error in lambda function: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

# Keep the original script for local execution
if __name__ == "__main__":
    # Call the lambda handler with empty event and context
    result = lambda_handler({}, None)
    print(result)