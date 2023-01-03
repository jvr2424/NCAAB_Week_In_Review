from sqlalchemy.sql import text
from sqlmodel import Session, select

import models
import serializers
from database import engine


def get_leagues(db: Session):

    statement = select(models.Leagues)
    results = db.exec(statement).all()

    return results


def get_weeks(db: Session):

    statement = select(models.Weeks)
    results = db.exec(statement).all()

    return results


def get_week(db: Session, week_number: int):

    statement = select(models.Weeks).where(models.Weeks.week_number == week_number)
    results = db.exec(statement).first()

    return results


def get_week_full_new(db: Session, league_id: int, week_number: int):
    statement = (
        select(models.WeeksFull)
        .where(models.WeeksFull.fr_week == week_number)
        .where(models.WeeksFull.fr_league_id == league_id)
    )
    results = db.exec(statement).all()

    return results
