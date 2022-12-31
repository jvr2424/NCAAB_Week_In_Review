from sqlalchemy.sql import text
from sqlmodel import Session, select

import models
from database import engine


def get_leagues(db: Session):

    statement = select(models.Leagues)
    results = db.exec(statement).all()
    print(results)
    return results


def get_weeks(db: Session):

    statement = select(models.Weeks)
    results = db.exec(statement).all()
    print(results)
    return results


def get_week(db: Session, week_number: int):

    statement = select(models.Weeks).where(models.Weeks.week_number == week_number)
    results = db.exec(statement).first()
    print(results)
    return results


def get_week_full(db: Session, league_id: int, week_number: int):
    # statement = select(models.Rankings).where(
    #     models.Rankings.league_id == league_id, models.Rankings.week == week_number
    # )
    # results = db.exec(statement).all()
    # print(results[0].espn_team.team_name)
    # print(results[0].schedule[0])

    # statement = (
    #     select(models.Rankings, models.Teams, models.Schedule)
    #     .where(
    #         models.Rankings.league_id == league_id, models.Rankings.week == week_number
    #     )
    #     .join(
    #         models.Teams,
    #         onclause=(
    #             models.Rankings.league_id == models.Teams.league_id
    #             and models.Rankings.espn_team_id == models.Teams.espn_team_id
    #         ),
    #         isouter=True,
    #     )
    #     .join(
    #         models.Schedule,
    #         onclause=(
    #             models.Rankings.league_id == models.Schedule.league_id
    #             and models.Rankings.espn_team_id == models.Schedule.espn_team_id
    #             and models.Rankings.week == models.Schedule.week_number
    #         ),
    #         isouter=True,
    #     )
    # )

    statement = f"""
        SELECT 
            fr.league_id as fr_league_id,
            fr.week as fr_week,
            fr.ranking as fr_ranking,
            fr.espn_team_id as fr_espn_team_id,
            fr.record as fr_record,
            fr_opt.league_id as fr_opt_league_id,
            fr_opt.week as fr_opt_week,
            fr_opt.ranking as fr_opt_ranking,
            fr_opt.espn_team_id as fr_opt_espn_team_id,
            fr_opt.record as fr_opt_record,
            ft.league_id as ft_league_id,
            ft.espn_team_id as ft_espn_team_id,
            ft.team_name as ft_team_name,
            ft.logo_url as ft_logo_url,
            ft_opp.league_id as ft_opp_league_id,
            ft_opp.espn_team_id as ft_opp_espn_team_id,
            ft_opp.team_name as ft_opp_team_name,
            ft_opp.logo_url as ft_opp_logo_url,
            fs.league_id as fs_league_id,
            fs.espn_team_id as fs_espn_team_id,
            fs.game_date as fs_game_date,
            fs.is_home as fs_is_home,
            fs.opponent_espn_team_id as fs_opponent_espn_team_id,
            fs.is_neutral_court as fs_is_neutral_court,
            fs.cancelled_or_postponed as fs_cancelled_or_postponed,
            fs.num_overtimes as fs_num_overtimes,
            fs.is_win as fs_is_win,
            fs.final_score as fs_final_score,
            fs.opponent_final_score as fs_opponent_final_score,
            fs.game_time as fs_game_time,
            fs.tv as fs_tv,
            fs.week_number as fs_week_number
        FROM fact_rankings as fr

        LEFT JOIN fact_teams as ft
        on ft.league_id = fr.league_id
        AND ft.espn_team_id = fr.espn_team_id

        LEFT JOIN fact_schedule as fs
        on fs.league_id = fr.league_id
        AND fs.espn_team_id = fr.espn_team_id
        AND fs.week_number = fr.week

        LEFT JOIN fact_teams as ft_opp
        on ft_opp.league_id = fs.league_id
        AND ft_opp.espn_team_id = fs.opponent_espn_team_id

        LEFT JOIN fact_rankings as fr_opt
        ON fs.league_id = fr_opt.league_id
        AND fs.opponent_espn_team_id = fr_opt.espn_team_id
        AND fs.week_number = fr_opt.week


        WHERE 
            fr.league_id = {league_id}
            AND fr.week = {week_number}
        ORDER BY fr.ranking, fs.game_date
    
    """
    results = db.exec(statement).all()
    print(dir(results[0]))
    print(results[0]._fields)
    for f in results[0]._fields:
        print(f)

    return results


def get_week_full(db: Session, league_id: int, week_number: int):
    # results = get_week(db, week_number=week_number)
    statement = select(models.Weeks).where(models.Weeks.week_number == week_number)
    results = db.exec(statement).first()
