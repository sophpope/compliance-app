from sqlalchemy import create_engine, NullPool
from sqlmodel import SQLModel, Session
from dotenv import load_dotenv
import os
from typing import Annotated
from fastapi import Depends



# Loading enviroment from .env
load_dotenv()

# Database connection

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?sslmode=require"

engine = create_engine(DATABASE_URL, poolclass=NullPool)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

