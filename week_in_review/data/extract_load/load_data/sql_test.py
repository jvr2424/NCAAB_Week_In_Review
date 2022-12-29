import sqlite3
import pandas as pd

con = sqlite3.connect('all_cbb_data_2-23_v1 copy.db')
cur = con.cursor()
# data =cur.execute('''
#     SELECT *  FROM team_schedule

# ''').fetchall()
# print(data)
### add column
# df = pd.read_sql_query("""SELECT *  FROM team_week_rankings
#                         WHERE ranking is NULL""", con)

# print(df.head())

pd.read_sql_query("""SELECT *  FROM team_schedule""", con).to_csv('ts2-24.csv')
pd.read_sql_query("""SELECT *  FROM teams""", con).to_csv('teams2-24.csv')
pd.read_sql_query("""SELECT *  FROM weeks""", con).to_csv('weaks2-24.csv')
pd.read_sql_query("""SELECT *  FROM team_week_rankings""", con).to_csv('twr2-24.csv')
