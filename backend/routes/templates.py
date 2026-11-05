from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from uuid import UUID

import models

from db_utils import SessionDep
from auth_utils import CurrentProfileDep

router = APIRouter()

@router.post('/add_template', response_model=models.ChecklistTemplatePublic)
def add_template(template_data: models.ChecklistTemplateCreate, 
                 current_profile: CurrentProfileDep, 
                 session: SessionDep):
    if template_data.visibility not in ['private', 'public']:
        raise HTTPException(status_code=400, detail="Invalid visibility value. Must be 'private' or 'public'.")
    
    template = models.ChecklistTemplates(
        **template_data.model_dump(), 
        account_id=current_profile.account_id,
        is_default=False)
    try:
        session.add(template)
        session.commit()
        session.refresh(template)
        return template
    except Exception as e:
        session.rollback()
        print("ADD TEMPLATE ERROR:")
        print(repr(e))
        raise