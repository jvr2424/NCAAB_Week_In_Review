from typing import Any, Optional

from sqlmodel import Field, Relationship, SQLModel


class Logs(SQLModel, table=True):
    __tablename__: str = "fact_logs"
    loaded_at: str = Field(primary_key=True)


class Leagues(SQLModel, table=True):
    __tablename__: str = "fact_leagues"
    league_id: int = Field(default=None, primary_key=True)
    league_name: str = Field()


class LeaguesDetail(Leagues):
    teams: list["Teams"] = Relationship(back_populates="league")


class Teams(SQLModel, table=True):
    __tablename__: str = "fact_teams"

    league_id: int = Field(
        default=None, primary_key=True, foreign_key="fact_leagues.league_id"
    )
    espn_team_id: int = Field(default=None, primary_key=True)
    team_name: str = Field()
    logo_url: str = Field


class TeamsDetail(Teams):
    league: Leagues = Relationship(back_populates="teams")
    ranking: list["Rankings"] = Relationship(back_populates="espn_team")
    # schedules: "Schedule" = Relationship(back_populates="team")


class Weeks(SQLModel, table=True):
    __tablename__: str = "fact_weeks"
    week_number: int = Field(default=None, primary_key=True)
    start_date: str = Field()
    end_date: str = Field()
    is_current_week: bool = Field()

    # schedules: "Schedule" = Relationship(back_populates="weeks")


class Rankings(SQLModel, table=True):
    __tablename__: str = "fact_rankings"
    league_id: int = Field(
        default=None, primary_key=True, foreign_key="fact_leagues.league_id"
    )
    week: int = Field(
        default=None, primary_key=True, foreign_key="fact_weeks.week_number"
    )
    ranking: int = Field(
        default=None,
        primary_key=True,
    )
    espn_team_id: int = Field(
        default=None, primary_key=True, foreign_key="fact_teams.espn_team_id"
    )
    record: str = Field()


class RankingsDetail(Rankings):
    espn_team: Teams = Relationship(back_populates="ranking")
    schedule: list["Schedule"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "and_(foreign(Schedule.week_number)==remote(Rankings.week), "
            "foreign(Schedule.league_id)==remote(Rankings.league_id), "
            "foreign(Schedule.espn_team_id)==remote(Rankings.espn_team_id))"
        },
    )


class Schedule(SQLModel, table=True):
    __tablename__: str = "fact_schedule"
    league_id: int = Field(
        default=None, primary_key=True, foreign_key="fact_leagues.league_id"
    )
    espn_team_id: int = Field(
        default=None, primary_key=True, foreign_key="fact_teams.espn_team_id"
    )
    game_date: str = Field()
    is_home: bool = Field
    opponent_espn_team_id: int = Field(
        default=None, primary_key=True, foreign_key="fact_teams.espn_team_id"
    )
    is_neutral_court: bool = Field()
    cancelled_or_postponed: bool = Field()
    num_overtimes: int = Field()
    is_win: bool = Field()
    final_score: int = Field()
    opponent_final_score: int = Field()
    game_time: str = Field()
    tv: str = Field()
    week_number: int = Field(
        default=None, primary_key=True, foreign_key="fact_weeks.week_number"
    )

    # ranking: Rankings = Relationship(
    #     back_populates="schedule",
    #     sa_relationship_kwargs={
    #         "primaryjoin": "and_(remote(Schedule.week_number)==foreign(Rankings.week), "
    #         "remote(Schedule.league_id)==foreign(Rankings.league_id), "
    #         "remote(Schedule.espn_team_id)==foreign(Rankings.espn_team_id))"
    #     },
    # )

    # weeks: Weeks = Relationship(back_populates="schedules")
    # team: Teams = Relationship(back_populates="schedules")
    # opponent: Teams = Relationship(back_populates="schedules")
