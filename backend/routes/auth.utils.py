import os

from dotenv import load_dotenv
from supabase import create_client

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