from fastapi import APIRouter, Depends
from sqlmodel import select
from uuid import UUID

import models
from db_utils import SessionDep
from auth_utils import CurrentProfileDep

router = APIRouter()

@router.get('/properties')
def get_properties(session:SessionDep):
    try:
        properties = session.exec(select(models.Properties)).all()
        return properties
    except Exception as e:
        return {"error": str(e)}
    
@router.post('/add_property', response_model=models.PropertyPublic)
def add_property(property_data: models.PropertyCreate, current_profile: CurrentProfileDep, session: SessionDep):
    property = models.Properties(**property_data.model_dump(), account_id=current_profile.account_id)
    try:
        session.add(property)
        session.commit()
        session.refresh(property)
        return property
    except Exception as e:
        session.rollback()
        print("ADD PROPERTY ERROR:")
        print(repr(e))
        raise
    
@router.get('/my_properties', response_model=list[models.PropertyPublic])
def get_my_properties(current_profile: CurrentProfileDep, session: SessionDep):
    try:
        properties = session.exec(select(models.Properties).where(models.Properties.account_id == current_profile.account_id)).all()
        return properties
    except Exception as e:
        return {"error": str(e)}