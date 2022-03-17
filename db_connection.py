from sqlalchemy import create_engine, text
import pandas as pd
import os


def get_connection():
    try:
        ps_connection = create_engine(os.getenv('POSTGRES_CONNECTION_STRING'))
        if ps_connection:
            print("successfully received connection from Postgres")
            ps_cursor = ps_connection.connect()
            return ps_cursor
    except Exception as error:
        print("Error while connecting to PostgreSQL aggregate db", error)
        return None


def execute_sql(sql: str, fetchone=False):
    connection = get_connection()
    data = pd.read_sql_query(sql=text(sql), con=connection).values
    if fetchone:
        data = [] if len(data) == 0 else data[0]
    return data


# test
if __name__ == '__main__':
    from dotenv import load_dotenv

    # load environment variables
    # load_dotenv()
    # db = get_connection()
    # print(db['users'].find_one())
