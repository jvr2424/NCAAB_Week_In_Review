from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Logs(BaseModel):
    loaded_at: datetime


class Leagues(BaseModel):
    league_id: int
    league_name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Teams(BaseModel):
    espn_team_id: int
    team_name: str
    logo_url: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TeamsDetail(Teams):
    league: Leagues


class Weeks(BaseModel):
    week_number: int
    start_date: Any
    end_date: Any
    is_current_week: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Rankings(BaseModel):
    league_id: int
    week: int
    ranking: int
    espn_team_id: int
    record: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RankingsDetail(Rankings):
    espn_team: Teams
    schedule: list["Schedule"]


class Schedule(BaseModel):
    league_id: int
    espn_team_id: int
    game_date: Any
    is_home: int
    opponent_espn_team_id: int
    is_neutral_court: bool | None
    cancelled_or_postponed: bool | None
    num_overtimes: int | None
    is_win: bool | None
    final_score: int | None
    opponent_final_score: int | None
    game_time: str | None
    tv: str | None
    week_number: int

    # weeks: Weeks
    # team: Teams
    # opponent: Teams

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class WeekRankingsSchedule(BaseModel):
    Rankings: Rankings
    Team: Teams

    class Config:
        orm_mode = True


RankingsDetail.update_forward_refs()
