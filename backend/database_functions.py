"""Functions that write to or query the mathnasium database"""

import psycopg2
from psycopg2.extensions import connection
from imports import (get_cursor, get_db_connection)

def get_student_attendance():
    """Queries the database for students that haven't attended"""

    conn = get_db_connection()
    curs = get_cursor(conn)

    curs.execute("""SELECT si.name, es.enrolment_status, si.mathnasium_id,
                si.student_link, a.account_name, a.account_link,
                ses.last_attendance, ses.attendance_count
                FROM student_information as si
                LEFT JOIN student_accounts AS sa ON si.student_id = sa.student_id
                LEFT JOIN accounts AS a ON sa.account_id = a.account_id
                LEFT JOIN student_education_stats AS ses ON si.student_id = ses.student_id
                LEFT JOIN enrolment_status AS es ON si.enrolment_id = es.enrolment_id
                WHERE ses.attendance_count < 5
                AND ses.last_attendance < CURRENT_DATE - INTERVAL '7 days'
                ;""")
    data = curs.fetchall()
    curs.close()
    conn.close()

    return data