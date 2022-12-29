import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import sqlite3
import re
import os
import load_database_functions

# # DB Structure

# ## Tables and Column    
# - Teams
#     - espn_team_id
#     - team_name
#     - logo_url
#     - team_page_url 
# - Team_Week_Rankings
#     - espn_team_id
#     - week_number
#     - ranking
# - Team_Schedule
#     - espn_team_id
#     - opponent_espn_team_id
#     - game_date
#     - is_home
#     - is_neutral_court
#     - is_win
#     - final_score
#     - opponent_final_score
#     - game_time
#     - tv
#     - cancelled_or_postponed
# - Weeks
#     - week_number
#     - start_date_inclusive
#     - end_date_exclusive
#     - is_current_week

#DATABASE_NAME = '../../db.sqlite3'
DATABASE_NAME = 'all_cbb_data_11_11_v1.db'

def setup_db(con):
    cur = con.cursor()

    # Create table https://www.sqlitetutorial.net/sqlite-foreign-key/
    cur.execute('''CREATE TABLE if not exists teams
                (espn_team_id integer PRIMARY KEY, team_name text, logo_url text, team_page_url text)''')

    cur.execute('''CREATE TABLE if not exists weeks
                ( week_number integer PRIMARY KEY, start_date_inclusive text, end_date_exclusive text, is_current_week integer)''')

    cur.execute('''CREATE TABLE if not exists team_week_rankings
                (id integer primary key AUTOINCREMENT,  espn_team_id integer, week_number integer, ranking integer,

                FOREIGN KEY (espn_team_id) 
                    REFERENCES teams (espn_team_id), 
                FOREIGN KEY (week_number) 
                    REFERENCES teams (week_number))''')

    cur.execute('''CREATE TABLE if not exists team_schedule
                (id integer primary key AUTOINCREMENT, espn_team_id integer, opponent_espn_team_id integer, week_number integer,
                game_date text, team_week_rankings_id integer, opponent_team_week_rankings_id integer, is_home integer, is_neutral_court integer, is_win integer,
                final_score integer, is_overtime integer, opponent_final_score integer,
                game_time text, tv text, cancelled_or_postponed integer,
                
                FOREIGN KEY (espn_team_id) 
                    REFERENCES teams (espn_team_id), 
                FOREIGN KEY (opponent_espn_team_id) 
                    REFERENCES teams (espn_team_id),
                FOREIGN KEY (week_number) 
                    REFERENCES teams (week_number),
                FOREIGN KEY (team_week_rankings_id)
                    REFERENCES team_week_rankings (id),
                FOREIGN KEY (opponent_team_week_rankings_id)
                    REFERENCES team_week_rankings (id))''')

    

    season_start_date = datetime.date(2022, 11, 7)
    season_end_date = datetime.date(2023, 3, 13)

    weeks_df = load_database_functions.create_weeks_table(con, season_start_date, season_end_date)
    print(weeks_df)
    # Insert a row of data
    #cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    con.commit()
    return con



def database_is_setup(con):
    cur = con.cursor()
    try:
        count = cur.execute("""SELECT COUNT(*) FROM weeks""").fetchall()[0][0]
        return count > 0 
    except:
        return False
    







def load_data_main():
    con = sqlite3.connect(DATABASE_NAME)
    #if os.path.exists(DATABASE_NAME):
    if database_is_setup(con):
        #incremental loads
        print('incremental load')
        #check if we have to update the current week
        week_was_updated = load_database_functions.update_latest_week(con)

        if week_was_updated:
            print('getting top 25 for new work')
            load_database_functions.load_top25_teams(con, load_database_functions.get_latest_week())


        #update schedule results only for teams that have been ranked
        all_teams = pd.read_sql_query("""SELECT DISTINCT t.espn_team_id 
                                        FROM teams as t 
                                        INNER JOIN team_week_rankings as twr 
                                        on t.espn_team_id = twr.espn_team_id""", con)
        for team in list(all_teams['espn_team_id']):
            print(f'checking for schedule updates for {team}')
            load_database_functions.load_or_update_schedule(con, team)
        
    else:
        #create from scratch
        setup_db(con)

        # get current week
        current_week = pd.read_sql_query("SELECT * from weeks WHERE is_current_week=1", con)['week_number'].values[0]
        #load all weeks data
        for week_num in range(1, current_week+1):
            load_database_functions.load_top25_teams(con, week_num)

        #get all teams and load their schedules
        all_teams = pd.read_sql_query("SELECT * from teams", con)
        for team in list(all_teams['espn_team_id']):
            load_database_functions.load_or_update_schedule(con, team)
        
        #get all teams that are in the schedule but not the teams table
        load_database_functions.add_teams_from_schedule(con)

    
    
    con.commit()
    con.close()

if __name__ == '__main__':
    load_data_main()