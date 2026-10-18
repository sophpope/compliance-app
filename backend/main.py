from fastapi import FastAPI

from routes import properties

app = FastAPI()

app.include_router(properties.router)

@app.get("/")
def root():
    return {"message": "Complaince API is running!"}




    



