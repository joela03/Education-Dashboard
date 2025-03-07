"""Function's that load pandas df to mathnasium database"""

import psycopg2 
import psycopg2.extras

# Database connection
conn = psycopg2.connect(host='localhost', user='joela0', dbname='mathnasium', port=5432)

def get_cursor(connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """Sets up cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)