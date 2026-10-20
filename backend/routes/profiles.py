from fastapi import APIRouter, Depends, HTTPException
from auth_utils import get_current_user
from uuid import UUID
from db_utils import SessionDep

import models

router = APIRouter()

@router.get('/me', response_model=models.ProfilePublic)
def get_my_profile(session: SessionDep, current_user=Depends(get_current_user)):
    profile = session.get(models.Profiles, UUID(str(current_user.id)))
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

