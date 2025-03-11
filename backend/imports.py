"""Function's that load pandas df to mathnasium database"""
import os
from dotenv import load_dotenv
import psycopg2 
import psycopg2.extras
from functions import (safe_date, percentage_to_float, ensure_list)

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
    
    status_mappings = {
        "enrolment": {
            "enrolled": 0,
            "on hold": 1
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
        enrolment_id = get_status_key('enrolment', enrolment_status)

        delivery_type = row.get('Delivery', '').strip()
        delivery_id = get_status_key('delivery', delivery_type)

        # Insert into student_information table
        curs.execute("""
            INSERT INTO student_information (name, mathnasium_id, student_link, enrolment_id, year)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (row['Student'], row.get('Mathnasium ID'), row['Student Link'], enrolment_id, row['Year']))
        student_id = curs.fetchone().get('id')
        conn.commit()

        # Insert into account table
        curs.execute("""
            INSERT INTO account (id, student_id, account_name, account_link)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (student_id) DO NOTHING;
        """, (row.get('Mathnasium ID'), student_id, row['Account Name'], row['Account Link']))
        conn.commit()

        # Insert into student_education_stats table
        curs.execute("""
            INSERT INTO student_education_stats (
                student_id, delivery_id, attendance_count, last_attendance, last_assessment,
                active_lps, skills_assigned, skills_mastered, last_lp_update, last_pr_sent,
                last_progress_check, mathnasium_id, total_lp_skills_mastered, total_lp_skills,
                skills_mastered_percent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            student_id, delivery_id, row['Attendance'],
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
                RETURNING id;
            """, (guardian_name.strip(), guardian_phone.strip()))
            guardian_id = curs.fetchone()[0]
            conn.commit()

            # Insert into student_guardians table
            curs.execute("""
                INSERT INTO student_guardians (student_id, guardian_id)
                VALUES (%s, %s)
                ON CONFLICT (student_id, guardian_id) DO NOTHING;
            """, (student_id, guardian_id))
            conn.commit()
