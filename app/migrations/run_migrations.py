import snowflake.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection details
DATABASE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
}

# Migration files
MIGRATIONS = [
    "app/migrations/001_create_users_table.sql"
]

def run_migrations():
    conn = snowflake.connector.connect(
        account=DATABASE_CONFIG['account'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database'],
        schema=DATABASE_CONFIG['schema'],
        warehouse=DATABASE_CONFIG['warehouse'],
    )

    try:
        cursor = conn.cursor()
        for migration in MIGRATIONS:
            with open(migration, 'r') as file:
                sql = file.read()
                cursor.execute(sql)
                print(f"Executed {migration}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_migrations()
