from fastapi import FastAPI

from routes import properties, profiles

app = FastAPI()

app.include_router(properties.router)
app.include_router(profiles.router)

@app.get("/")
def root():
    return {"message": "Complaince API is running!"}




    



