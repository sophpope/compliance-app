from fastapi import FastAPI
from sqlalchemy import text
from db_utils import engine
import models
from db_utils import SessionDep
from sqlmodel import select

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Complaince API is running!"}

@app.get('/properties')
def get_properties(session:SessionDep):
    try:
        properties = session.exec(select(models.Properties)).all()
        return properties
    except Exception as e:
        return {"error": str(e)}


    



