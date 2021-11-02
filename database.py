import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

con = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='eninf')

engine = create_engine("mysql+pymysql://root@localhost/eninf")

df = pd.read_sql('holidays', con = engine)       # reading from the database

print(df.head())
# year_df.to_sql("yearly consumption", con=engine, if_exists="replace", index=False)      # writing to the database