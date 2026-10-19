import os

from dotenv import load_dotenv
from supabase import create_client
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SUPABASE_URL = os.getenv("supbase_url")
SUPABASE_PUBLISHABLE_KEY = os.getenv("supbase_publishable_key")

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