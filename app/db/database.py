import snowflake.connector
from app.config import develop

def get_db():
    conn = snowflake.connector.connect(
        account=develop.DATABASE['account'],
        user=develop.DATABASE['user'],
        password=develop.DATABASE['password'],
        database=develop.DATABASE['database'],
        schema=develop.DATABASE['schema'],
        warehouse=develop.DATABASE['warehouse'],
    )
    try:
        print(develop.DATABASE['user'])
        yield conn.cursor()
        # yield conn
        # yield cursor
    finally:
        # cursor.close()
        conn.close()
