import os 
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("ERROR: The environment variable 'DB_URL' is not configured in the .env file")


# Connection pool: Create 1 to 10 connections to the database for faster response times
try:
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=DATABASE_URL,
    )
except Exception as e:
    print(f"Error creating connection pool: {e}")
    connection_pool = None


@contextmanager
def get_db_connection():
    """Get and return a connection from the connection pool"""
    conn = connection_pool.getconn() # Get a connection from the pool
    try:
        yield conn # Yield the connection to the context manager
    finally:
        connection_pool.putconn(conn) # After the 'with' block, return the connection to the pool


# Cursor: A pointer to the database that can execute queries
@contextmanager
def get_db_cursor():
    """Get and return a cursor from the connection"""
    # Before creating the cursor, get a connection from the pool
    with get_db_connection() as conn:
        # Use RealDictCursor to return results as dictionaries
        with conn.cursor(cursor_factory=RealDictCursor) as cursor: 
            yield cursor