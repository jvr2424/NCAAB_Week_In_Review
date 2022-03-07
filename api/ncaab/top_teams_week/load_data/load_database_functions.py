import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import sqlite3
import re

CURRENT_SEASON = 2021
LATEST_RANKINGS_URL = 'https://www.espn.com/mens-college-basketball/rankings'
WEEKLY_RANKINGS_URL = f'https://www.espn.com/mens-college-basketball/rankings/_/week/WEEK_NUMBER/year/{CURRENT_SEASON+1}/seasontype/2' #'https://www.espn.com/mens-college-basketball/rankings/_/week/15/year/2022/seasontype/2'
TEAM_SCHEDULE_URL = 'https://www.espn.com/mens-college-basketball/team/schedule/_/id/TEAM_ID' #replace TEAM_ID with espn_team_id
TEAM_HOME_URL = '/mens-college-basketball/team/_/id/TEAM_ID' #replace TEAM_ID with espn_team_id
LOGO_URL = 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/TEAM_ID.png&w=40&h=40' #replace TEAM_ID with espn_team_id


def load_top25_teams(con, week_number):
    '''loads the teams and team_week_rankings tables '''
    # - Teams
    #     - espn_team_id
    #     - team_name
    #     - logo_url
    #     - team_page_url
    # 
    # - Team_Week_Rankings
        # - espn_team_id
        # - week_number
        # - ranking  
    rank_res = requests.get(WEEKLY_RANKINGS_URL.replace('WEEK_NUMBER', str(week_number)))
    soup = BeautifulSoup(rank_res.content, 'lxml')
    table = soup.find('div', attrs={'class':'Table__Title'}, text='AP Top 25').parent.find('table')
    tbody_rows = table.find('tbody').find_all('tr')
    
    top_25 =[]
    for row in tbody_rows:
        col_count = 1
        this_team = {}
        for col in row.find_all('td'):
            if col_count == 1:
                #rank
                this_team['ranking'] = col.text
                if col.text.strip() =='':
                    this_team['ranking'] = int(top_25[-1]['ranking'])+1
                
            elif col_count == 2:
                #logo + team name
                this_team['logo_url'] = col.find('img').attrs['src']
                this_team['team_name'] = col.find_all('span')[2].text
                this_team['team_page_url'] = col.find_all('span')[2].find('a').attrs['href']
                
            elif col_count == 3:
                #record
                this_team['record'] = col.text
                
            elif col_count == 4:
                #pts
                pass
            elif col_count == 5:
                #trend
                pass
            col_count += 1
        top_25.append(this_team)


    df = pd.DataFrame(top_25)

    df['espn_team_id'] = df['team_page_url'].str.extract(r'_/id/([0-9]+)').astype(int)
    df['week_number'] = week_number

    existing_teams_df = pd.read_sql_query("SELECT * from teams", con)
    teams_df = df[['espn_team_id', 'team_name','logo_url','team_page_url' ]].copy()
    teams_df = teams_df[~teams_df['espn_team_id'].isin(existing_teams_df['espn_team_id'])].copy()

    teams_df.to_sql('teams', con, if_exists='append', index=False )
    
    
    existing_team_week_rankings = pd.read_sql_query("SELECT * from team_week_rankings", con)
    team_week_rankings = df[['espn_team_id', 'week_number','ranking']].copy()

    # team_week_rankings = team_week_rankings[~(team_week_rankings['espn_team_id'].isin(existing_team_week_rankings['espn_team_id'])) &
    #                                         ~(team_week_rankings['week_number'].isin(existing_team_week_rankings['week_number']))]


    team_week_rankings.to_sql('team_week_rankings', con, if_exists='append', index=False )

    con.commit()
    
    return teams_df, team_week_rankings, existing_team_week_rankings




def load_or_update_schedule(con, espn_team_id):
    if espn_team_id >0:
        '''loads the schedule table for new teams and udpates results for existing teams'''
        cur = con.cursor()

        team_schedule_response = requests.get(TEAM_SCHEDULE_URL.replace('TEAM_ID', str(espn_team_id)))
        soup = BeautifulSoup(team_schedule_response.content, 'lxml')
        table = soup.find('table')
        game_is_final = True
        date_header_count = 0
        all_games = []
        print()
            

        regex = re.compile(r"([0-9]*)OT", re.IGNORECASE)

        for row in table.find_all('tr'):
            game_cancelled_or_postponed = False
            all_cols = row.find_all('td')
            if all_cols[0].text=='DATE':
                date_header_count+=1

            if date_header_count == 2:
                game_is_final = False

            if len(all_cols)>1 and all_cols[0].text!='DATE':
                print(f"Game Results for {espn_team_id}: {all_cols[0].text}")
                if all_cols[2].text.lower() == 'canceled' or all_cols[2].text.lower() == 'postponed':
                    game_cancelled_or_postponed = True
                
                this_game = {'espn_team_id': espn_team_id}
                col_count = 1
                
                for col in all_cols:
                    if col_count == 1:
                        #date
                        game_date = datetime.datetime.strptime(col.text, "%a, %b %d")
                        if game_date.date() < datetime.date(1900,5,1):
                            game_date = game_date + datetime.timedelta(365.25* (CURRENT_SEASON-1900+1))
                        else:
                            game_date = game_date + datetime.timedelta(365.25*(CURRENT_SEASON-1900))


                        this_game['game_date'] = game_date.strftime("%Y-%m-%d") #game_date.isoformat() #game_date.strftime("%m-%d-%y")
                    elif col_count == 2:
                        #opponent_espn_team_id
                        #is_home
                        #is_neutral_court
                        spans = col.find_all('span')
                        this_game['is_home'] = spans[0].text == 'vs' and '*' not in spans[2].text
                        try:
                            this_game['opponent_espn_team_id'] = int(re.search(r'_/id/([0-9]+)', spans[1].find('a').attrs['href']).group(1))
                        except:
                            #check if this team name exists
                            opponent_team_name_no_id = spans[2].text.replace('*', '')
                            opponent_team_name_created_id = cur.execute(f"""SELECT espn_team_id FROM teams
                                                         WHERE team_name = '{opponent_team_name_no_id}'""").fetchone()

                            if opponent_team_name_created_id:
                                print(f"found created team id {opponent_team_name_created_id[0]}")
                                this_game['opponent_espn_team_id'] = opponent_team_name_created_id[0]
                            else:
                                #check if any team exits with -1 or less and add it to the teams table
                                smallest_id = cur.execute('SELECT min(espn_team_id) FROM teams').fetchone()[0]
                                if smallest_id < 0:
                                    new_id = smallest_id-1
                                else:
                                    new_id = -1
                                cur.execute(f"INSERT INTO teams VALUES ({new_id},'{opponent_team_name_no_id}', NULL, NULL)")
                                this_game['opponent_espn_team_id'] = new_id

                        this_game['is_neutral_court'] = '*' in spans[2].text 
                    elif col_count == 3:
                        if game_is_final:
                            this_game['cancelled_or_postponed'] = game_cancelled_or_postponed
                            if game_cancelled_or_postponed:
                                this_game['is_win'] = None
                                this_game['final_score'] = None
                                this_game['opponent_final_score'] = None
                                this_game['is_overtime'] = None
                                this_game['game_time'] = None
                                this_game['tv'] = None
                                
                            else:
                                #is_win
                                #final_score
                                #opponent_final_score
                                #is_overtime
                                spans = col.find_all('span')
                                matches = regex.search( spans[1].text.split('-')[1].strip())
                                if matches:
                                    this_game['is_overtime'] = matches.group(1).strip() #spans[1].text.split('-')[1].strip().endswith('OT')
                                else:
                                    this_game['is_overtime'] =0

                                
                                this_game['is_win'] = spans[0].text == 'W'
                                if this_game['is_win']:
                                    this_game['final_score'] = spans[1].text.split('-')[0]
                                    this_game['opponent_final_score'] = regex.sub("", spans[1].text.split('-')[1]).strip()#spans[1].text.split('-')[1].replace(' OT', '')
                                else:
                                    this_game['final_score'] = regex.sub("", spans[1].text.split('-')[1]).strip()#spans[1].text.split('-')[1].replace(' OT', '')
                                    this_game['opponent_final_score'] = spans[1].text.split('-')[0]
                                
                                
                                this_game['game_time'] = None
                                this_game['tv'] = None

                        else:
                            # game_time 
                            # tv
                            spans = col.find_all('span')
                            this_game['game_time'] = spans[0].text
                            this_game['tv'] = None
                            
                            this_game['is_win'] = None
                            this_game['final_score'] = None
                            this_game['opponent_final_score'] = None

                    col_count +=1
                
                #add week number
                if this_game['game_date']:
                    #date_str = datetime.datetime.fromisoformat('2021-11-09T06:00:00').strftime('%Y-%m-%d')
                    date_str = this_game['game_date']
                    week_q = f"""SELECT week_number FROM weeks WHERE '{date_str}'>= start_date_inclusive and '{date_str}'< end_date_exclusive"""
                    #print(week_q)
                    #print(this_game)
                    week_number = cur.execute(week_q).fetchone()[0]
                    this_game['week_number'] = week_number

                #add team_week_rankings_id
                twr_query = f"""SELECT id FROM team_week_rankings
                                WHERE espn_team_id={espn_team_id} and week_number={this_game['week_number']}"""

                twr_id = cur.execute(twr_query).fetchone()
                if twr_id:
                    this_game['team_week_rankings_id'] = twr_id[0]
                else:
                    this_game['team_week_rankings_id'] = None

                #add opponent_team_week_rankings_id
                opp_twr_query = f"""SELECT id FROM team_week_rankings
                                WHERE espn_team_id={this_game['opponent_espn_team_id']} and week_number={this_game['week_number']}"""
                
                opp_twr_id = cur.execute(opp_twr_query).fetchone()
                if opp_twr_id:
                    this_game['opponent_team_week_rankings_id'] = opp_twr_id[0]
                else:
                    this_game['opponent_team_week_rankings_id'] = None
                
                all_games.append(this_game)

        lastest_df = pd.DataFrame(all_games)

        #- team_schedule
            # - espn_team_id
            # - opponent_espn_team_id
            # - game_date
            # - is_home
            # - is_neutral_court
            # - is_win
            # - final_score
            
            # - opponent_final_score
            # - is_overtime

        sql_query = f'SELECT * FROM team_schedule WHERE espn_team_id = {espn_team_id}'
        existing_df = pd.read_sql_query(sql_query, con)

        #get existing schedule for team
        #if none exists add the current schedule

        if len(existing_df) ==0:
            lastest_df.to_sql('team_schedule', con, if_exists='append', index=False) 

        else:
            # import pdb
            # pdb.set_trace()
            
            lastest_df[['is_home', 'is_neutral_court', 'cancelled_or_postponed', 'is_win']]=lastest_df[['is_home', 'is_neutral_court', 'cancelled_or_postponed', 'is_win']].stack().map({True:1,False:0}).unstack()
            existing_df = existing_df.drop(columns='id')
            lastest_df = lastest_df.replace('',np.nan)

            for col in existing_df.columns:
                if lastest_df[col].isna().sum() > 0 and existing_df[col].dtype == np.int64:
                    print(col)
                    lastest_df[col] = lastest_df[col].astype(float)
                else:
                    lastest_df[col] = lastest_df[col].astype(existing_df[col].dtype)


            updated_rows = pd.concat([existing_df, lastest_df], sort=False).drop_duplicates(keep=False)
            dates_to_update = list(updated_rows['game_date'].unique())
            

           
            for date in dates_to_update:
                print(date)
                updated_date_value = lastest_df[lastest_df['game_date']== date]

                if str(updated_date_value['is_overtime'].values[0]).strip() == '':
                    overtime_value = 'NULL'
                else:
                    overtime_value =updated_date_value['is_overtime'].values[0]

                update_query = f"""UPDATE team_schedule
                            SET is_win = {updated_date_value['is_win'].values[0]},
                                final_score = {updated_date_value['final_score'].values[0]},
                                opponent_final_score = {updated_date_value['opponent_final_score'].values[0]},
                                cancelled_or_postponed = {updated_date_value['cancelled_or_postponed'].values[0]},
                                opponent_espn_team_id = {updated_date_value['opponent_espn_team_id'].values[0]},
                                is_home =  {updated_date_value['is_home'].values[0]},
                                is_neutral_court =  {updated_date_value['is_neutral_court'].values[0]},
                                is_overtime = {overtime_value}

                        WHERE
                            espn_team_id = {espn_team_id} and
                            game_date = '{date}'
                """.replace(' = nan', ' = NULL')
                print(update_query)
                cur.execute(update_query)
                


def get_latest_week():
    rank_res = requests.get(LATEST_RANKINGS_URL)
    soup = BeautifulSoup(rank_res.content, 'lxml')
    # get latest week
    latest_week = soup.select_one('div.dropdown:nth-child(2) > select:nth-child(2)').find_all('option')[-1].attrs['value'].replace('Week ', '')
    return latest_week

def update_latest_week(con):

    current_db_week = pd.read_sql_query("SELECT * from weeks WHERE is_current_week=1", con)
    latest_week = get_latest_week()

    needs_update = False

    if int(latest_week) != int(list(current_db_week['week_number'])[0]):
        needs_update = True
        print(f'updating current week from {latest_week} to {list(current_db_week["week_number"])[0]}')
        cur = con.cursor()
        #set the last week to 0
        cur.execute("""UPDATE weeks
                            SET is_current_week = 0
                        WHERE
                            is_current_week = 1
                """)

        #set the new week to 1
        cur.execute(f"""UPDATE weeks
                            SET is_current_week = 1
                        WHERE
                            week_number = {latest_week}
                """)
        con.commit()

    return needs_update
        



    
    
def create_weeks_table(con, start_date, end_date):
    # - Weeks
    #     - week_number
    #     - start_date_inclusive
    #     - end_date_exclusive
    
    latest_week = get_latest_week()

    print(f"latest_week: {latest_week}")
    num_weeks = (end_date - start_date).days/7
    #season_start_date = datetime.date(2021,11,8)
    #season_start_date.strftime("%m-%d-%y")

    start_date_inclusive = start_date
    end_date_exclusive = start_date_inclusive +datetime.timedelta(days=7)
    

    all_weeks = []
    for week_number in range(1,int(num_weeks) +1):
        all_weeks.append({
            'week_number': week_number,
            'start_date_inclusive': start_date_inclusive.isoformat(), #start_date_inclusive.strftime("%m-%d-%y"),
            'end_date_exclusive': end_date_exclusive.isoformat(), #end_date_exclusive.strftime("%m-%d-%y"),
            'is_current_week' : week_number == int(latest_week)
        })

        start_date_inclusive =start_date_inclusive +datetime.timedelta(days=7)
        end_date_exclusive = start_date_inclusive +datetime.timedelta(days=7)
            
        
    weeks_df = pd.DataFrame(all_weeks)

    weeks_df.to_sql('weeks',con, if_exists='replace',  index=False)

    return weeks_df


def add_teams_from_schedule(con):
    all_teams = pd.read_sql_query('''SELECT DISTINCT opponent_espn_team_id
                                    FROM team_schedule as ts
                                    LEFT JOIN teams as t on ts.opponent_espn_team_id=t.espn_team_id
                                    WHERE t.espn_team_id is NULL''', con)
    cur = con.cursor()

    for team_id in all_teams['opponent_espn_team_id']:
        team_response = requests.get(TEAM_SCHEDULE_URL.replace('TEAM_ID', str(team_id)))

        soup = BeautifulSoup(team_response.content, 'lxml')
        team_name = soup.find('h1', attrs={'class': 'ClubhouseHeader__Name' }).find('span').find('span').text.replace("'", "''")
        logo_url = LOGO_URL.replace('TEAM_ID', str(team_id))
        team_page_url = TEAM_HOME_URL.replace('TEAM_ID', str(team_id))

        query_str = f"INSERT INTO teams VALUES ({team_id},'{team_name}', '{logo_url}', '{team_page_url}')"
        cur.execute(query_str)
    con.commit()

    