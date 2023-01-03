from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import queries
import schemas
import serializers
from database import Session, engine

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/leagues", response_model=list[schemas.Leagues])
async def leagues(db: Session = Depends(get_db)):
    """
    returns all leagues from database
    """
    return queries.get_leagues(db)


@app.get("/weeks", response_model=list[schemas.Weeks])
async def weeks(db: Session = Depends(get_db)):
    """
    returns all weeks from database
    """
    return queries.get_weeks(db)


@app.get("/weeks_full/{week_num}")
async def weeks_full_new(week_num: int, league_id: int, db: Session = Depends(get_db)):
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

    res = queries.get_week_full_new(db, league_id=league_id, week_number=week_num)

    final_res = serializers.nest_week_rankings(res)
    return final_res
