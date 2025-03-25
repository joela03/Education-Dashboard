"""Function's that load pandas df to mathnasium database"""
import os
import hashlib
from dotenv import load_dotenv
import psycopg2 
import psycopg2.extras
from functions import (safe_date, percentage_to_float, ensure_list,
                    add_mathnasium_id_column)

def get_db_connection():
    """Sets up connection with database"""

    # Load environment variables
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")
    db_password = os.getenv("DB_PASSWORD")

    # Check if all environment variables
    if not all([db_host, db_user, db_name, db_port, db_password]):
        raise ValueError("Missing required environment variables for DB connection.")
    
    # Establish and return the connection
    return psycopg2.connect(host=db_host, user=db_user, dbname=db_name, port=db_port, password=db_password)

def get_cursor(connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """Sets up cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def get_status_key(status_type: str, status: str) -> int | None:
    """Returns a key based on the given status type and value."""

    if not isinstance(status_type, str) or not isinstance(status, str):
        return None
    
    status_mappings = {
        "enrolment": {
            "enrolment": 0,
            "on hold": 1,
            "pre-enroled": 2,
        },
        "delivery": {
            "in-centre": 0,
            "@home": 1
        }
    }

    return status_mappings.get(status_type.lower(), {}).get(status.lower())

def import_students_to_database(conn, df):
    """Imports students from dataframe to the database"""

    curs = get_cursor(conn)

    for _, row in df.iterrows():
        # Convert Enrolment Status and Delivery to keys
        enrolment_status = row.get('Enrolment Status', '').strip()
        enrolment_key = get_status_key('enrolment', enrolment_status)

        delivery_type = row.get('Delivery', '').strip()
        delivery_id = get_status_key('delivery', delivery_type)

        # Insert into student_information table
        curs.execute("""
            INSERT INTO student_information (name, mathnasium_id, student_link,
                    delivery_id, year)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (mathnasium_id) DO UPDATE 
            SET name = EXCLUDED.name,
                student_link = EXCLUDED.student_link,
                delivery_id = EXCLUDED.delivery_id,
                year = EXCLUDED.year
            RETURNING student_id;
        """, (row['Student'],
            row.get('Mathnasium ID'),
            row['Student Link'],
            delivery_id,
            0 if row['Year'] == "Reception" else (13 if row['Year'] == "College" else row['Year']),
            ))
        student_id = curs.fetchone().get('student_id')
        conn.commit()

        # Insert into accounts table
        curs.execute("""
            INSERT INTO accounts (account_name, account_link)
            VALUES (%s, %s)
            ON CONFLICT (account_name) DO NOTHING
            RETURNING account_id;
        """, (row['Account Name'], row['Account Link']))
        account = curs.fetchone()
        conn.commit()

        if account:
            account_id = account['account_id']
        else:
            # Fetch existing account_id if no insertions
            curs.execute("SELECT account_id FROM accounts WHERE account_name = %s", (row['Account Name'],))
            account = curs.fetchone()
            if account:
                account_id = account['account_id']
            else:
                raise ValueError("Failed to retrieve account_id for account_name:", row['Account Name'])

        conn.commit()
        
        # Insert into student_accounts table
        curs.execute("""
            INSERT INTO student_accounts (student_id, account_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (student_id, account_id))
        conn.commit()

        # Insert into student_education_stats table
        curs.execute("""
            INSERT INTO student_education_stats (
                student_id, attendance_count, last_attendance, last_assessment,
                active_lps, skills_assigned, skills_mastered, last_lp_update, last_pr_sent,
                last_progress_check, mathnasium_id, total_lp_skills_mastered, total_lp_skills,
                skills_mastered_percent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id) DO UPDATE 
            SET attendance_count = EXCLUDED.attendance_count,
                last_attendance = EXCLUDED.last_attendance,
                last_assessment = EXCLUDED.last_assessment,
                active_lps = EXCLUDED.active_lps,
                skills_assigned = EXCLUDED.skills_assigned,
                skills_mastered = EXCLUDED.skills_mastered,
                last_lp_update = EXCLUDED.last_lp_update,
                last_pr_sent = EXCLUDED.last_pr_sent,
                last_progress_check = EXCLUDED.last_progress_check,
                mathnasium_id = EXCLUDED.mathnasium_id,
                total_lp_skills_mastered = EXCLUDED.total_lp_skills_mastered,
                total_lp_skills = EXCLUDED.total_lp_skills,
                skills_mastered_percent = EXCLUDED.skills_mastered_percent;
        """, (
            student_id, row['Attendance'],
            safe_date(row['Last Attendance']),
            safe_date(row['Last Assessment']),
            row['Active LPs'],
            row['Skills Assigned'], row['Skills Mastered'],
            safe_date(row['Last LP Update']),
            safe_date(row['Last PR Sent']),
            safe_date(row['Last Progress Check']),
            row['Mathnasium ID'], row['Total LP Skills Mastered'],
            row['Total LP Skills'], percentage_to_float(row['% Skills Mastered'])
        ))
        conn.commit()

        # Insert guardians and student_guardians
        guardians = row.get('Guardians', [])
        guardian_phones = row.get('Guardian Phone Numbers', [])

        guardians = ensure_list(row.get('Guardians'))
        guardian_phones = ensure_list(row.get('Guardian Phone Numbers'))
        
        for guardian_name, guardian_phone in zip(guardians, guardian_phones):
            curs.execute("""
                INSERT INTO guardians (guardian_name, guardian_phone)
                VALUES (%s, %s)
                ON CONFLICT (guardian_name) DO UPDATE 
                SET guardian_phone = EXCLUDED.guardian_phone
                RETURNING guardian_id;
            """, (guardian_name.strip(), guardian_phone.strip()))
            guardian_id = curs.fetchone().get('guardian_id')
            conn.commit()

            # Insert into student_guardians table
            curs.execute("""
                INSERT INTO student_guardians (student_id, guardian_id)
                VALUES (%s, %s)
                ON CONFLICT (student_id, guardian_id) DO NOTHING;
            """, (student_id, guardian_id))
            conn.commit()
            
def hash_password(password: str) -> tuple:
    """Hashes password with a salt"""
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(),
                                    salt, 100000)
    
    return {"salt": salt.hex(), "password_hash": hash_bytes.hex()}

def verify_password(stored_salt: str, stored_hash: str, password: str) -> bool:
    """Verifies submitted password"""
    
    salt = bytes.fromhex(stored_salt)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return stored_hash == hash_bytes.hex()

def insert_user(username: str, password: str, conn):
    salt, password_hash = hash_password(password)
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO users (username, password_hash, salt)
                VALUES (%s, %s, %s)""", (username, password_hash, salt)
            )
            conn.commit()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def get_student_id(conn, mathnasium_id: int) -> int:
    """Retrieves id of a student given a mathnasium id"""

    try:
        with conn.cursor() as curs:
            curs.execute(
                """SELECT student_id
                FROM student_information
                WHERE mathnasium_id = %s""",
                (mathnasium_id,)
            )
            result = curs.fetchone()
            return result[0] if result else None
    except psycopg2.Error as e:
        print(f"An error occured: {e}")
        conn.rollback()
        return None
    
def insert_preenroled_into_students(conn, df):
    """Inserts student with a status of pre-enroled into the students database"""

    try:

        for _, row in df.iterrows():
                delivery_type = row.get('Current Status').strip()
                delivery_id = get_status_key('delivery', delivery_type)

                with conn.cursor() as curs:
                    curs.execute("""
                    INSERT INTO student_information (name, mathnasium_id, student_link,
                            delivery_id, year)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (mathnasium_id) DO UPDATE 
                    SET name = EXCLUDED.name,
                        student_link = EXCLUDED.student_link,
                        delivery_id = EXCLUDED.delivery_id,
                        year = EXCLUDED.year;
                """, (row.get('Student'),
                    row.get('Mathnasium ID'),
                    row.get('Student Link'),
                    delivery_id,
                    0 if row.get('Year') == "Reception" else (13 if row.get('Year') == "College" else row.get('Year')),
                    ))

        conn.commit()
 
    except psycopg2.Error as e:
        print(f"An error occured: {e}")
        conn.rollback()
        return None
    
def insert_into_assessments_db(conn, df):
    """Inserts assessments into assessment db"""

    try:
        for _, row in df.iterrows():
            student_id = get_student_id(conn, row.get("Mathnasium ID"))
            if not student_id:
                print(f"Skipping assessment entry for missing student ID: {row.get('Mathnasium ID')}")
                continue

            score = percentage_to_float(row.get("Score"))

            with conn.cursor() as curs:
                # Insert into assessments table
                curs.execute("""
                    INSERT INTO assessments (date_taken, assessment_title,
                                            assessment_level, score)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (date_taken, assessment_title, assessment_level) DO UPDATE
                    SET date_taken = EXCLUDED.date_taken,
                        assessment_title = EXCLUDED.assessment_title,
                        assessment_level = EXCLUDED.assessment_level,
                        score = EXCLUDED.score
                    RETURNING assessment_id;
                """, (
                    row.get("Date Taken"),
                    row.get("Assessment Title"),
                    row.get("Assessment Level"),
                    score
                ))

                # Extract assessment_id
                result = curs.fetchone()
                if result:
                    assessment_id = result[0]

                    # Insert into assessments_students table
                    curs.execute("""
                        INSERT INTO assessments_students (assessment_id, student_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (assessment_id, student_id))

            conn.commit()
    
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return None

def insert_into_enrolments_db(conn, df):
    """Inserts enrolments into the enrolments database."""
    
    try:
        with conn.cursor() as curs:
            for _, row in df.iterrows():
                student_id = get_student_id(conn, row.get("Mathnasium ID"))
                if not student_id:
                    print(f"Skipping enrolment entry for missing student ID: {row.get('Mathnasium ID')}")
                    continue

                enrolment_key = get_status_key("enrolment", row.get("Current Status", ""))

                # Insert into enrolments table
                curs.execute("""
                    INSERT INTO enrolments (student_id, enrolment_key, membership,
                                            enrolment_start, enrolment_end, total_hold_length)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (student_id, enrolment_key) DO UPDATE
                    SET membership = EXCLUDED.membership,
                        enrolment_start = EXCLUDED.enrolment_start,
                        enrolment_end = EXCLUDED.enrolment_end,
                        total_hold_length = EXCLUDED.total_hold_length
                    RETURNING enrolment_id;
                """, (
                    student_id,
                    enrolment_key,
                    row.get("Membership Type"),
                    row.get("Enrollment Start"),
                    row.get("Enrollment End"),
                    row.get("Total Hold Length")
                ))

        conn.commit()
    
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return None