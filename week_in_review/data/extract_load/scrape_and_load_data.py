import datetime
import os
import re
from dataclasses import dataclass, field

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

CURRENT_SEASON = 2022
MENS_PATH = "mens-college-basketball"
WOMENS_PATH = "womens-college-basketball"
BASE_LATEST_RANKINGS_URL = "https://www.espn.com/%s/rankings"
BASE_WEEKLY_RANKINGS_URL = f"https://www.espn.com/%s/rankings/_/week/WEEK_NUMBER/year/{CURRENT_SEASON+1}/seasontype/2"  #'https://www.espn.com/mens-college-basketball/rankings/_/week/15/year/2022/seasontype/2'
BASE_TEAM_SCHEDULE_URL = "https://www.espn.com/%s/team/schedule/_/id/TEAM_ID"  # replace TEAM_ID with espn_team_id
BASE_TEAM_HOME_URL = "/%s/team/_/id/TEAM_ID"  # replace TEAM_ID with espn_team_id
LOGO_URL = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/TEAM_ID.png&w=40&h=40"  # replace TEAM_ID with espn_team_id


@dataclass
class EspnUrls:
    PATH: str
    LATEST_RANKINGS_URL: str = field(init=False)
    WEEKLY_RANKINGS_URL: str = field(init=False)
    TEAM_SCHEDULE_URL: str = field(init=False)
    TEAM_HOME_URL: str = field(init=False)
    base_path: str = field(init=False)

    def __post_init__(self):
        self.LATEST_RANKINGS_URL = BASE_LATEST_RANKINGS_URL % self.PATH
        self.WEEKLY_RANKINGS_URL = BASE_WEEKLY_RANKINGS_URL % self.PATH
        self.TEAM_SCHEDULE_URL = BASE_TEAM_SCHEDULE_URL % self.PATH
        self.TEAM_HOME_URL = BASE_TEAM_HOME_URL % self.PATH
        idx = self.PATH.find("-")
        self.base_path = self.PATH[:idx]

    # def __init__(self, path: str) -> None:
    #     self.PATH = path
    #     self.LATEST_RANKINGS_URL = BASE_LATEST_RANKINGS_URL % self.PATH
    #     self.WEEKLY_RANKINGS_URL = BASE_WEEKLY_RANKINGS_URL % self.PATH
    #     self.TEAM_SCHEDULE_URL = BASE_TEAM_SCHEDULE_URL % self.PATH
    #     self.TEAM_HOME_URL = BASE_TEAM_HOME_URL % self.PATH

    def __str__(self) -> str:
        return self.base_path

    # @property
    # def base_path(self) -> str:
    #     idx = self.PATH.find("-")
    #     return self.PATH[:idx]


MENS_URLS = EspnUrls(MENS_PATH)
WOMENS_URLS = EspnUrls(WOMENS_PATH)

MENS_RANKINGS_TABLE_NAME = f"raw_{MENS_URLS.base_path}_week_rankings"
WOMENS_RANKINGS_TABLE_NAME = f"raw_{WOMENS_URLS.base_path}_week_rankings"

MENS_SCHEDULE_TABLE_NAME = f"raw_{MENS_URLS.base_path}_schedules"
WOMENS_SCHEDULE_TABLE_NAME = f"raw_{WOMENS_URLS.base_path}_schedules"


def write_to_db(df: pd.DataFrame, table_name: str):
    # "postgresql://postgres:example@172.02.2.3/raw"

    conn_string = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@postgres/{os.environ['POSTGRES_DB']}"
    db = create_engine(conn_string)
    conn = db.connect()
    df.to_sql(table_name, con=conn, if_exists="replace", index=False)


def main():
    """
    entry point for all scraping functions
    """
    # mens data
    men_ranking_df = get_rankings(MENS_URLS)
    write_to_db(men_ranking_df, MENS_RANKINGS_TABLE_NAME)

    men_schedule_df = get_schedules(MENS_URLS, men_ranking_df)
    write_to_db(men_schedule_df, MENS_SCHEDULE_TABLE_NAME)

    # womens data
    women_ranking_df = get_rankings(WOMENS_URLS)
    write_to_db(women_ranking_df, WOMENS_RANKINGS_TABLE_NAME)

    women_schedule_df = get_schedules(WOMENS_URLS, women_ranking_df)
    write_to_db(women_schedule_df, MENS_RANKINGS_TABLE_NAME)


def get_rankings(urls: EspnUrls) -> pd.DataFrame:
    all_rankings = []
    for week_num in range(1, 21):
        print(week_num)
        try:
            all_rankings += load_top25_teams(urls, week_num)
        except ValueError as v_er:
            print(v_er)
            break
    # with open("test_rankings.json", "w", encoding="utf-8") as f:
    #     f.write(json.dumps(all_rankings))

    # get the unique teams
    # get their schedules
    df = pd.DataFrame(all_rankings)
    return df


def get_schedules(urls: EspnUrls, rankings_df: pd.DataFrame) -> pd.DataFrame:
    rankings_df = rankings_df.drop_duplicates("team_name")

    all_schedules = []
    for row_idx, team in rankings_df.iterrows():
        match = re.search("id/([0-9]+)/", team["team_page_url"])
        if match:
            espn_team_id = int(match.group(1))
            all_schedules += load_or_update_schedule(urls, espn_team_id=espn_team_id)

    # with open("test_schedules.json", "w", encoding="utf-8") as f:
    #     f.write(json.dumps(all_schedules))
    schedule_df = pd.DataFrame(all_schedules)
    return schedule_df


def load_or_update_schedule(urls: EspnUrls, espn_team_id: str) -> list[dict[str, str]]:
    if espn_team_id > 0:

        team_schedule_response = requests.get(
            urls.TEAM_SCHEDULE_URL.replace("TEAM_ID", str(espn_team_id)), timeout=30
        )
        soup = BeautifulSoup(team_schedule_response.content, "lxml")
        table = soup.find("table")
        game_is_final = True
        date_header_count = 0
        all_games = []

        regex = re.compile(r"([0-9]*)OT", re.IGNORECASE)

        for row in table.find_all("tr"):
            game_cancelled_or_postponed = False
            all_cols = row.find_all("td")
            if all_cols[0].text == "DATE":
                date_header_count += 1

            if date_header_count == 2:
                game_is_final = False

            if len(all_cols) > 1 and all_cols[0].text != "DATE":
                if (
                    all_cols[2].text.lower() == "canceled"
                    or all_cols[2].text.lower() == "postponed"
                ):
                    game_cancelled_or_postponed = True

                this_game = {"espn_team_id": espn_team_id}
                col_count = 1

                for col in all_cols:
                    if col_count == 1:
                        # date
                        game_date = datetime.datetime.strptime(col.text, "%a, %b %d")
                        if game_date.date() < datetime.date(1900, 5, 1):
                            game_date = game_date + datetime.timedelta(
                                365.25 * (CURRENT_SEASON - 1900 + 1)
                            )
                        else:
                            game_date = game_date + datetime.timedelta(
                                365.25 * (CURRENT_SEASON - 1900)
                            )

                        this_game["game_date"] = game_date.strftime(
                            "%Y-%m-%d"
                        )  # game_date.isoformat() #game_date.strftime("%m-%d-%y")
                    elif col_count == 2:
                        # opponent_espn_team_id
                        # is_home
                        # is_neutral_court
                        spans = col.find_all("span")
                        this_game["is_home"] = (
                            spans[0].text == "vs" and "*" not in spans[2].text
                        )
                        opponent_a = spans[-1].find("a")
                        if opponent_a:
                            try:
                                this_game["opponent_espn_team_id"] = int(
                                    re.search(
                                        r"_/id/([0-9]+)", opponent_a.attrs["href"]
                                    ).group(1)
                                )
                            except:
                                this_game["opponent_espn_team_id"] = -1

                            this_game["opponent_team_name"] = opponent_a.text
                            this_game["opponent_logo_url"] = LOGO_URL.replace(
                                "TEAM_ID", str(this_game["opponent_espn_team_id"])
                            )

                        else:
                            this_game["opponent_espn_team_id"] = -1
                            this_game["opponent_team_name"] = spans[-1].text
                            this_game["opponent_logo_url"] = None

                        this_game["is_neutral_court"] = "*" in spans[2].text
                    elif col_count == 3:
                        if game_is_final:
                            this_game[
                                "cancelled_or_postponed"
                            ] = game_cancelled_or_postponed
                            if game_cancelled_or_postponed:
                                this_game["is_win"] = None
                                this_game["final_score"] = None
                                this_game["opponent_final_score"] = None
                                this_game["is_overtime"] = None
                                this_game["game_time"] = None
                                this_game["tv"] = None

                            else:
                                # is_win
                                # final_score
                                # opponent_final_score
                                # is_overtime
                                spans = col.find_all("span")
                                matches = regex.search(
                                    spans[1].text.split("-")[1].strip()
                                )
                                if matches:
                                    this_game["is_overtime"] = matches.group(
                                        1
                                    ).strip()  # spans[1].text.split('-')[1].strip().endswith('OT')
                                else:
                                    this_game["is_overtime"] = 0

                                this_game["is_win"] = spans[0].text == "W"
                                if this_game["is_win"]:
                                    this_game["final_score"] = spans[1].text.split("-")[
                                        0
                                    ]
                                    this_game["opponent_final_score"] = regex.sub(
                                        "", spans[1].text.split("-")[1]
                                    ).strip()  # spans[1].text.split('-')[1].replace(' OT', '')
                                else:
                                    this_game["final_score"] = regex.sub(
                                        "", spans[1].text.split("-")[1]
                                    ).strip()  # spans[1].text.split('-')[1].replace(' OT', '')
                                    this_game["opponent_final_score"] = spans[
                                        1
                                    ].text.split("-")[0]

                                this_game["game_time"] = None
                                this_game["tv"] = None

                        else:
                            # game_time
                            # tv
                            spans = col.find_all("span")
                            this_game["game_time"] = spans[0].text
                            this_game["tv"] = None

                            this_game["is_win"] = None
                            this_game["final_score"] = None
                            this_game["opponent_final_score"] = None

                    col_count += 1

                all_games.append(this_game)
        return all_games


def load_top25_teams(urls: EspnUrls, week_number: int) -> list[dict[str, str]]:
    rank_res = requests.get(
        urls.WEEKLY_RANKINGS_URL.replace("WEEK_NUMBER", str(week_number)), timeout=30
    )
    if rank_res.status_code != 200:
        raise ValueError("Week not found")
    soup = BeautifulSoup(rank_res.content, "lxml")
    for elem in soup.find_all("div"):
        if elem.text == "No Data Available":
            raise ValueError("Week not found")

    table = soup.find(
        "div", attrs={"class": "Table__Title"}, text="AP Top 25"
    ).parent.find("table")
    tbody_rows = table.find("tbody").find_all("tr")

    top_25 = []
    for row in tbody_rows:
        col_count = 1
        this_team = {"week": week_number}
        for col in row.find_all("td"):
            if col_count == 1:
                # rank
                this_team["ranking"] = col.text
                if col.text.strip() == "":
                    this_team["ranking"] = int(top_25[-1]["ranking"]) + 1

            elif col_count == 2:
                # logo + team name
                this_team["logo_url"] = col.find("img").attrs["src"]
                this_team["team_name"] = col.find_all("span")[2].text
                this_team["team_page_url"] = (
                    col.find_all("span")[2].find("a").attrs["href"]
                )

            elif col_count == 3:
                # record
                this_team["record"] = col.text

            elif col_count == 4:
                # pts
                pass
            elif col_count == 5:
                # trend
                pass
            col_count += 1
        top_25.append(this_team)

    return top_25


if __name__ == "__main__":
    main()
