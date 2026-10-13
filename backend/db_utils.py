from fastapi import FastAPI
from sqlalchemy import create_engine, NullPool
from dotenv import load_dotenv
import os
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Complaince API is running!"}

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

try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed to {e}")

