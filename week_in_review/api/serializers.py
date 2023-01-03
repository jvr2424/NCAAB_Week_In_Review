import json

import pandas as pd

import models


def nest_week_rankings(response: list[models.WeeksFull]):
    prefixs = {
        "fr_": None,
        "fs_": None,
        "ft_": None,
        "ft_opp_": None,
    }

    """
    [
        {
            ranking:1,
            team: {
                id:1,
                name:UNC
                url:www...

            },
            schedule: [
                {
                    game
                }
            ]
        }
    ]
    """

    # get unique teams (should be 25)
    all_items = []
    print(response)

    for item in response:
        this_item = {}
        for key in item.dict().keys():
            this_item[key] = getattr(item, key)
        all_items.append(this_item)

    all_items_str = json.dumps(all_items, default=str)
    all_items = json.loads(all_items_str)

    df = (
        pd.DataFrame(all_items)
        .fillna("")
        .replace("", None)
    )
    print(df.columns)
    df = df.sort_values(["fr_ranking", "fs_game_date"])
    print(df)

    top_25_df = (
        df.drop_duplicates(["fr_ranking", "fr_espn_team_id"])
        .copy()
        .reset_index(drop=True)
    )
    # [["fr_league_id", "fr_week", "fr_ranking", "fr_espn_team_id"]    ]
    print(top_25_df)

    final_data = []
    for _, ranked_team in top_25_df.iterrows():
        this_team_rank = {
            "ranking": ranked_team["fr_ranking"],
            "espn_team": {
                "id": ranked_team["fr_espn_team_id"],
                "team_name": ranked_team["ft_team_name"],
                "logo_url": ranked_team["ft_logo_url"],
            },
            "schedule": [],
        }
        temp_slice = df.loc[
            (df["fr_ranking"] == ranked_team["fr_ranking"])
            & (df["fr_espn_team_id"] == ranked_team["fr_espn_team_id"])
        ]

        all_games = []
        for _, team_game in temp_slice.iterrows():
            this_game = {
                "game_date": team_game["fs_game_date"],
                "opponent_espn_team": {
                    "id": team_game["ft_opp_espn_team_id"],
                    "team_name": team_game["ft_opp_team_name"],
                    "logo_url": team_game["ft_opp_logo_url"],
                },
                "opponent_week_ranking": team_game["fr_opt_ranking"],
                "is_home": team_game["fs_is_home"],
                "is_neutral_court": team_game["fs_is_neutral_court"],
                "cancelled_or_postponed": team_game["fs_cancelled_or_postponed"],
                "num_overtimes": team_game["fs_num_overtimes"],
                "is_win": team_game["fs_is_win"],
                "final_score": team_game["fs_final_score"],
                "opponent_final_score": team_game["fs_opponent_final_score"],
                "game_time": team_game["fs_game_time"],
                "tv": team_game["fs_tv"],
                "week_number": team_game["fs_week_number"],
            }
            all_games.append(this_game)
        this_team_rank["schedule"] = all_games
        final_data.append(this_team_rank)
    return {"rankings": final_data}
