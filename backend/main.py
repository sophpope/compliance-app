from fastapi import FastAPI
from sqlalchemy import text
from db_utils import engine

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Complaince API is running!"}

@app.get('/properties')
def get_properties():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM properties"))
        properties = [dict(row._mapping) for row in result]
    return properties
