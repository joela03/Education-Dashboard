"""Functions that write to or query the mathnasium database"""

import psycopg2
from psycopg2.extensions import connection

def get_connection() -> connection:
    """Sets up connection"""
    return psycopg2.connect(
        "dbname=mathnasium user=joela0 host=localhost")