from fastapi import APIRouter, Depends, HTTPException
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
    
@router.get('/property/{property_id}', response_model=models.PropertyPublic)
def get_property(property_id: UUID, current_profile: CurrentProfileDep, session: SessionDep):
    try:
        property = session.exec(select(models.Properties).where(models.Properties.id == property_id, models.Properties.account_id == current_profile.account_id)).first()
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
        if property.account_id != current_profile.account_id:
            raise HTTPException(status_code=403, detail="You do not have access to this property")
        return property
    
    except Exception as e:
        print("GET PROPERTY ERROR:", repr(e))

        raise HTTPException(status_code=404, detail="Unable to retrieve property")
    
@router.patch("/property/{property_id}", response_model=models.PropertyPublic)
def update_property(
    property_id: UUID, 
    property_data: models.PropertyUpdate, 
    current_profile: CurrentProfileDep, 
    session: SessionDep
):
    try:
        property = session.exec(select(models.Properties).where(
            models.Properties.id == property_id, 
            models.Properties.account_id == current_profile.account_id)).first()
        
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
        
        update_data = property_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(property, key, value)

        session.add(property)
        session.commit()
        session.refresh(property)

        return property
    
    except Exception as e:
        print("UPDATE PROPERTY ERROR:", repr(e))
        raise HTTPException(status_code=400, detail="Unable to update property")