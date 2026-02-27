import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env
load_dotenv()

def init_database():
    # 1. Get individual fields (Consistency with .env.example)
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "proggy_wallet")

    # 2. Construct URLs
    # Base URL connects to 'postgres' to create the target database
    base_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/postgres"
    
    # Final URL for applying the schema
    db_url = os.getenv("DATABASE_URL") or f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    print(f"Starting database initialization for '{db_name}'...")

    try:
        # 3. Connect to 'postgres' database to create the new one
        conn = psycopg2.connect(base_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name}")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()

        # 4. Connect to the new database and apply schema
        print(f"Applying schema from backend/database/schema.sql...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        schema_path = Path("backend/database/schema.sql")
        if schema_path.exists():
            with open(schema_path, "r") as f:
                cursor.execute(f.read())
            conn.commit()
            print("Schema applied successfully!")
        else:
            print("Error: backend/database/schema.sql not found.")

        cursor.close()
        conn.close()
        print("Database is ready to use!")

    except Exception as e:
        print(f"Error during initialization: {e}")

if __name__ == "__main__":
    init_database()
