"""Function's that load pandas df to mathnasium database"""
import os
from dotenv import load_dotenv
import psycopg2 
import psycopg2.extras

# Database connection
def get_db_connection():
    "Sets up connection with database"

    # Load environment variables
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")

    # Check if all environment variables
    if not all([db_host, db_user, db_name, db_port]):
        raise ValueError("Missing required environment variables for DB connection.")
    
    # Establish and return the connection
    return psycopg2.connect(host=db_host, user=db_user, dbname=db_name, port=db_port)

def get_cursor(connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """Sets up cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def get_enrolment_key(conn, enrolment: str) -> int:
    """Gets genre key"""
    curs = get_cursor(conn)
    curs.execute("""SELECT enrolment_id
                   FROM enrolment_status
                   WHERE enrolment_status LIKE %s;""",
                 (enrolment,))
    data = curs.fetchone()
    curs.close()

    if data:
        return data["enrolment_id"]

    return None