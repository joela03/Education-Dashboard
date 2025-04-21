from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from imports import get_cursor, get_db_connection

def get_username_data(username: str):
    """Queries db for relevant student data"""
    conn = get_db_connection()
    curs = get_cursor(conn)
    
    curs.execute("""
        SELECT salt, password_hash
        FROM users
        WHERE username = %s
    """, (username,))
    data = curs.fetchone()
    
    curs.close()
    conn.close()
    
    return dict(data) if data else None

def get_student_attendance():
    """Queries the database for students that haven't attended"""
    conn = get_db_connection()
    curs = get_cursor(conn)
    
    curs.execute("""
        SELECT si.name, es.enrolment_status, si.mathnasium_id,
               si.student_link, a.account_name, a.account_link,
               ses.last_attendance, ses.attendance_count
        FROM student_information AS si
        LEFT JOIN student_accounts AS sa ON si.student_id = sa.student_id
        LEFT JOIN accounts AS a ON sa.account_id = a.account_id
        LEFT JOIN student_education_stats AS ses ON si.student_id = ses.student_id
        LEFT JOIN enrolments AS e ON si.student_id = e.student_id
        LEFT JOIN enrolment_status AS es ON e.enrolment_key = es.enrolment_key
        WHERE ses.attendance_count < 5
           OR ses.last_attendance < CURRENT_DATE - INTERVAL '7 days'
    """)
    
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    return data

def get_progress_check():
    """Query the database for students that need a progress check"""
    conn = get_db_connection()
    curs = get_cursor(conn)
    
    curs.execute("""
        SELECT si.name, es.enrolment_status, si.mathnasium_id,
               si.student_link, ses.last_assessment, ses.last_progress_check,
               ses.skills_mastered_percent
        FROM student_information AS si
        LEFT JOIN student_education_stats AS ses ON si.student_id = ses.student_id
        LEFT JOIN enrolments AS e ON si.student_id = e.student_id
        LEFT JOIN enrolment_status AS es ON e.enrolment_key = es.enrolment_key
        LEFT JOIN LATERAL (
            SELECT a.assessment_id, a.assessment_title, a.assessment_level,
                a.date_taken
            FROM 
                assessments_students ast
            JOIN 
                assessments a ON ast.assessment_id = a.assessment_id
            WHERE 
                ast.student_id = si.student_id
                AND a.assessment_level ~ '^[0-9]+$'
            ORDER BY 
                a.date_taken DESC
            LIMIT 1
        ) a ON true
        WHERE 
            ((a.date_taken < CURRENT_DATE - INTERVAL '3 months'
                    AND ses.last_progress_check < CURRENT_DATE - INTERVAL '3 months')
                OR
                (ses.skills_mastered_percent > 45
                    AND ses.last_progress_check < CURRENT_DATE - INTERVAL '3 months')
            )
        ORDER BY 
            si.name
        """)
    
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    return data

def get_checkup_data():
    """Queries the database for students that need a post checkup"""
    conn = get_db_connection()
    curs = get_cursor(conn)
    
    curs.execute("""
        SELECT si.name, es.enrolment_status, si.mathnasium_id,
               si.student_link, ses.last_assessment, ses.skills_mastered_percent
        FROM student_information AS si
        LEFT JOIN student_education_stats AS ses ON si.student_id = ses.student_id
        LEFT JOIN enrolments AS e ON si.student_id = e.student_id
        LEFT JOIN enrolment_status AS es ON e.enrolment_key = es.enrolment_key
        LEFT JOIN LATERAL (
            SELECT a.assessment_id, a.assessment_title, a.assessment_level,
                a.date_taken
            FROM 
                assessments_students ast
            JOIN 
                assessments a ON ast.assessment_id = a.assessment_id
            WHERE 
                ast.student_id = si.student_id
                AND a.assessment_level ~ '^[0-9]+$'
            ORDER BY 
                a.date_taken DESC
            LIMIT 1
        ) a ON true
        WHERE 
            ((a.date_taken < CURRENT_DATE - INTERVAL '6 months')
                OR
                (ses.skills_mastered_percent > 90)
            )
        ORDER BY 
            si.name
        """)
    
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    return data

def get_plan_pace():
    """Queries the database for students that aren't on pace"""
    conn = get_db_connection()
    curs = get_cursor(conn)
    
    curs.execute("""
        SELECT si.name, es.enrolment_status, si.mathnasium_id,
               si.student_link, ses.last_assessment, ses.skills_mastered_percent
        FROM student_information AS si
        LEFT JOIN student_education_stats AS ses ON si.student_id = ses.student_id
        LEFT JOIN enrolments AS e ON si.student_id = e.student_id
        LEFT JOIN enrolment_status AS es ON e.enrolment_key = es.enrolment_key
        WHERE (EXTRACT(DAY FROM (CURRENT_DATE::timestamp - ses.last_assessment::timestamp)) / 7) * 4 > ses.skills_mastered_percent
    """)
    
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    return data

def get_care_call():
    """Query to retrieve useful information for a carecall"""

    conn = get_db_connection()
    curs = get_cursor(conn)

    curs.execute("""
        SELECT si.name, es.enrolment_status, si.student_link,
            ses.skills_mastered_percent, ses.skills_assigned,
            ses.skills_mastered, e.total_hold_length,
            a.assessment_title as last_core_assessment,
            a.date_taken as last_core_assessment_date,
            a.score as last_core_assessment_score
        FROM student_information AS si
        LEFT JOIN student_education_stats AS ses ON si.student_id = ses.student_id
        LEFT JOIN enrolments AS e ON si.student_id = e.student_id
        LEFT JOIN enrolment_status AS es ON e.enrolment_key = es.enrolment_key
        LEFT JOIN LATERAL (
            SELECT 
                a.assessment_title, 
                a.date_taken,
                a.score
            FROM 
                assessments_students ast
            JOIN 
                assessments a ON ast.assessment_id = a.assessment_id
            WHERE 
                ast.student_id = si.student_id
                AND a.assessment_level ~ '^[0-9]+$'
            ORDER BY 
                a.date_taken DESC
            LIMIT 1
        ) a ON true
        """)
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    return data

def get_enrolment_stats():
    """Queries for student counts"""

    conn = get_db_connection()
    curs = get_cursor(conn)

    curs.execute("""
        SELECT COUNT(*)
        FROM enrolments
        WHERE enrolment_key  = 0;
    """)

    enrolment_count = curs.fetchone()["count"]
    print(enrolment_count)

    curs.execute("""
        SELECT COUNT(*)
        FROM enrolments
        WHERE enrolment_key  = 1;
    """)

    hold_count = curs.fetchone()["count"]

    curs.execute("""
        SELECT COUNT(*)
        FROM enrolments
        WHERE enrolment_key  = 2;
    """)

    pre_enroled_count = curs.fetchone()["count"]

    first_day_prev_month = datetime.now().replace(day=1) - relativedelta(months=1)
    first_day_curr_month = datetime.now().replace(day=1)

    curs.execute("""
        SELECT COUNT(*)
        FROM enrolments
        WHERE enrolment_start >= %s
        AND enrolment_start < %s
    """, (first_day_prev_month, first_day_curr_month))

    previous_month_enrolments = curs.fetchone()["count"]

    curs.execute("""
        SELECT AVG(attendance_count) as total_attendance
        FROM student_education_stats
    """)

    avg_attendance = curs.fetchone()["total_attendance"]

    curs.close()

    return [{
        "active_enrolment": enrolment_count,
        "on_hold": hold_count,
        "pre_enroled": pre_enroled_count,
        "previous_month_enrolments": previous_month_enrolments,
        "avg_attendance": avg_attendance
    }]

def get_education_level_stats():
    """Pulls stats on education"""

    conn = get_db_connection()
    curs = get_cursor(conn)

    curs.execute("""
        SELECT si.student_id, si.year, latest_assessment.assessment_level, e.enrolment_start
        FROM student_information si
        JOIN enrolments as e ON e.student_id = si.student_id
        LEFT JOIN LATERAL (
            SELECT a.assessment_level
            FROM assessments_students ast
            JOIN assessments a ON ast.assessment_id = a.assessment_id
            WHERE ast.student_id = si.student_id
            AND a.assessment_level ~ '^[0-9]+$'
            ORDER BY a.date_taken DESC
            LIMIT 1
        ) latest_assessment ON true
        WHERE latest_assessment.assessment_level IS NOT NULL;
    """)

    data = curs.fetchall()

    curs.close()

    return data
