from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    String,
    Time,
)
from sqlalchemy.orm import object_session, relationship

from database import declarative_base

# metadata_obj = MetaData(schema='public_fact')

Base = declarative_base()


class Leagues(Base):
    __tablename__ = "fact_leagues"

    league_id = Column(Integer, primary_key=True, index=True)
    league_name = Column(String, unique=True)


class Logs(Base):
    __tablename__ = "fact_logs"

    loaded_at = Column(Time, primary_key=True, index=True)


class Rankings(Base):
    __tablename__ = "fact_rankings"
    # __table_args__ = (
    #     ForeignKeyConstraint(
    #         ["league_id", "espn_team_id"],
    #         ["fact_teams.league_id", "fact_teams.espn_team_id"],
    #     ),
    # )
    league_id = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)
    ranking = Column(Integer, primary_key=True)
    espn_team_id = Column(
        Integer, ForeignKey("fact_teams.espn_team_id"), primary_key=True
    )
    record = Column(String)

    # team = relationship("Teams")
    # week_rel = relationship(
    #     "Weeks",
    #     primaryjoin="Rankings.week==Weeks.week_number",
    #     back_populates="rankings",
    # )

    @property
    def team(self):
        s = """
            SELECT ft.*
            FROM fact_teams as ft
            INNER JOIN fact_rankings as fr
            ON ft.league_id = fr.league_id and ft.espn_team_id = fr.espn_team_id
            """
        # WHERE fr.league_id = :p_league_id and fr.espn_team_id = :p_team_id
        result = (
            object_session(self)
            .execute(
                s,
                params={"p_league_id": self.league_id, "p_team_id": self.espn_team_id},
            )
            .fetchall()
        )
        print(result)
        return result

    @property
    def week_rel(self):
        s = """
            SELECT fw.*
            FROM fact_weeks as fw
            INNER JOIN fact_rankings as fr
            ON fw.week_number = fr.week
            """
        # WHERE fr.week_number = :week_id
        result = (
            object_session(self).execute(s, params={"week_id": self.week}).fetchall()
        )
        print(result)
        return result


class Schedule(Base):
    __tablename__ = "fact_schedule"
    # __table_args__ = (
    #     ForeignKeyConstraint(
    #         ["league_id", "espn_team_id"],
    #         ["fact_teams.league_id", "fact_teams.espn_team_id"],
    #     ),
    #     ForeignKeyConstraint(
    #         ["league_id", "opponent_espn_team_id"],
    #         ["fact_teams.league_id", "fact_teams.espn_team_id"],
    #     ),
    # )

    league_id = Column(Integer, primary_key=True)
    espn_team_id = Column(
        Integer, ForeignKey("fact_teams.espn_team_id"), primary_key=True
    )
    game_date = Column(Date, primary_key=True)
    is_home = Column(Boolean)

    is_neutral_court = Column(Boolean)
    cancelled_or_postponed = Column(Boolean)
    num_overtimes = Column(Integer)
    is_win = Column(Boolean)
    final_score = Column(Integer)
    opponent_espn_team_id = Column(
        Integer, ForeignKey("fact_teams.espn_team_id"), primary_key=True
    )
    opponent_final_score = Column(Integer)
    game_time = Column(String)
    tv = Column(String)
    week_number = Column(Integer, ForeignKey("fact_weeks.week_number"))

    weeks = relationship("Weeks")
    team = relationship("Teams", foreign_keys=[espn_team_id])
    opponent = relationship("Teams", foreign_keys=[opponent_espn_team_id])


class Teams(Base):
    __tablename__ = "fact_teams"
    league_id = Column(
        Integer,
        ForeignKey("fact_leagues.league_id"),
        primary_key=True,
    )
    espn_team_id = Column(Integer, primary_key=True)
    team_name = Column(String)
    logo_url = Column(String)

    league = relationship("Leagues")


class Weeks(Base):
    __tablename__ = "fact_weeks"
    week_number = Column(
        Integer,
        primary_key=True,
    )
    start_date = Column(Date)
    end_date = Column(Date)
    is_current_week = Column(Boolean)
