from fastapi import APIRouter, Depends
from sqlmodel import select
from uuid import UUID

import models
from db_utils import SessionDep

router = APIRouter()

@router.get('/properties')
def get_properties(session:SessionDep):
    try:
        properties = session.exec(select(models.Properties)).all()
        return properties
    except Exception as e:
        return {"error": str(e)}
    
@router.post('/add_property', response_model=models.PropertyPublic)
def add_property(property: models.PropertyCreate, account_id:UUID, session: SessionDep):
    property = models.Property(**property.model_dump(), account_id=account_id)
    try:
        session.add(property)
        session.commit()
        session.refresh(property)
        return property
    except Exception as e:
        return {"error": str(e)}