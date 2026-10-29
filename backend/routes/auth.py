from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth_utils import supabase 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                #username is email for supabase 
                "email": form_data.username,
                "password": form_data.password
             
            }
        )

        if not response.session:
            raise HTTPException(status_code = 401, detail = "Invalid email or password")
        
        return{
            "access_token": response.session.access_token, 
            "token_type": "bearer"
        }
    
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )