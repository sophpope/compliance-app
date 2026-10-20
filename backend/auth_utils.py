import os

from dotenv import load_dotenv
from supabase import create_client
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import models
from db_utils import SessionDep
from uuid import UUID
from typing import Annotated

load_dotenv()

SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_PUBLISHABLE_KEY = os.getenv("supabase_publishable_key")

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing")

if not SUPABASE_PUBLISHABLE_KEY:
    raise ValueError("SUPABASE_PUBLISHABLE_KEY is missing")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY
)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    try:
        response = supabase.auth.get_user(token)

        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return response.user
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token"
)
    
def get_current_profile(session: SessionDep, current_user=Depends(get_current_user)):
    profile = session.get(models.Profiles, UUID(str(current_user.id)))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

CurrentProfileDep = Annotated[models.Profiles, Depends(get_current_profile)]