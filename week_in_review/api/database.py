import os

from sqlmodel import Session, create_engine

dbschema = "public_fact"  # Searches left-to-right

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@postgres/{os.environ['POSTGRES_DB']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"options": "-csearch_path={}".format(dbschema)},
)
