import psycopg2
import os

def get_db_connection() -> psycopg2.extensions.connection:
    """
    Creates and returns a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'postgres'),  # Use 'postgres' as service name
            database=os.getenv('POSTGRES_DB', 'serviceScope_db'),
            user=os.getenv('POSTGRES_USER', 'admin@localhost.com'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Unable to connect to database: {e}")
        return None
