from fastapi import APIRouter, Depends
from auth_utils import get_current_user

router = APIRouter()

@router.get('/me')
def get_my_profile(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}

