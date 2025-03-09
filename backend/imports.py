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
    
    # Establish and return the connection
    return psycopg2.connect(host=db_host, user=db_user, dbname=db_name, port=db_port)

def get_cursor(connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """Sets up cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)