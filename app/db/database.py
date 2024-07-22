import snowflake.connector
from app.config import develop

def get_db():
    """
        Generator function to create and manage a database connection using Snowflake.

        This function handles the connection to a Snowflake database using credentials
        stored in a development configuration module. It yields a cursor object that can
        be used to execute queries. After the business logic is executed, it ensures that
        the connection is properly closed, regardless of whether an exception occurred.

        Yields:
        snowflake.connector.cursor: A cursor object from the established Snowflake connection.

        The function uses a try-finally block to ensure that the connection is closed properly.
        This is crucial in web applications to prevent database connection leaks which can lead
        to performance issues.
    """
    conn = snowflake.connector.connect(
        account=develop.DATABASE['account'],
        user=develop.DATABASE['user'],
        password=develop.DATABASE['password'],
        database=develop.DATABASE['database'],
        schema=develop.DATABASE['schema'],
        warehouse=develop.DATABASE['warehouse'],
    )
    try:
        yield conn.cursor()
    finally:
        conn.close()
