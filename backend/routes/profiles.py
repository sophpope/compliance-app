from fastapi import APIRouter, Depends, HTTPException
from auth_utils import get_current_user
from uuid import UUID
from db_utils import SessionDep
from auth_utils import CurrentProfileDep

import models

router = APIRouter()

@router.get('/me', response_model=models.ProfilePublic)
def get_my_profile(current_profile: CurrentProfileDep):
    return current_profile

