from fastapi import FastAPI

from routes import properties, profiles, auth, property_assets

app = FastAPI()

app.include_router(properties.router)
app.include_router(profiles.router)
app.include_router(auth.router)
app.include_router(property_assets.router)

@app.get("/")
def root():
    return {"message": "Complaince API is running!"}




    



