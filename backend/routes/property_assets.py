from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from uuid import UUID

import models

from db_utils import SessionDep
from auth_utils import CurrentProfileDep

router = APIRouter()

@router.post('/add_property_asset/{property_id}', response_model=models.PropertyAssetPublic)      
def add_property_asset(
    property_asset_data: models.PropertyAssetCreate, 
    property_id: UUID, 
    current_profile: CurrentProfileDep, 
    session: SessionDep):
    property = session.exec(
        select(models.Properties).where(
            models.Properties.id == property_id,
            models.Properties.account_id == current_profile.account_id
        )).first()
    
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    
    property_asset = models.PropertyAssets(**property_asset_data.model_dump(), 
                                           property_id=property_id)
    try:
        session.add(property_asset)
        session.commit()
        session.refresh(property_asset)
        return property_asset
    except Exception as e:
        session.rollback()
        print("ADD PROPERTY ASSET ERROR:")
        print(repr(e))
        raise

@router.get('/property_assets/{property_id}', response_model=list[models.PropertyAssetPublic])
def get_property_assets(property_id: UUID,
                        current_profile: CurrentProfileDep, 
                        session: SessionDep):
    
    property = session.exec(
        select(models.Properties).where(
            models.Properties.id == property_id,
            models.Properties.account_id == current_profile.account_id
        )).first()
    
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found / You do not have access to this property")

    try:
        property_assets = session.exec(
            select(models.PropertyAssets)
            .where(
                models.PropertyAssets.property_id == property_id)
        ).all()
        return property_assets
    
    except Exception as e:
        print("GET PROPERTY ASSET ERROR:", repr(e))

        raise HTTPException(status_code=404, detail="Unable to retrieve property asset")
    

@router.patch("/property_asset/{property_asset_id}", response_model=models.PropertyAssetPublic)
def update_property_asset(
    property_asset_id: UUID, 
    property_asset_data: models.PropertyAssetUpdate, 
    current_profile: CurrentProfileDep, 
    session: SessionDep
):
    try:
        property_asset = session.exec(select(models.PropertyAssets).where(
            models.PropertyAssets.id == property_asset_id)).first()
        
        if property_asset is None:
            raise HTTPException(status_code=404, detail="Property Asset not found")
        
        # Check if the property asset belongs to a property owned by the current profile
        property = session.exec(
            select(models.Properties).where(
                models.Properties.id == property_asset.property_id,
                models.Properties.account_id == current_profile.account_id
            )).first()
        
        if property is None:
            raise HTTPException(status_code=403, detail="You do not have access to this property asset")
        
        for key, value in property_asset_data.model_dump(exclude_unset=True).items():
            setattr(property_asset, key, value)
        
        session.add(property_asset)
        session.commit()
        session.refresh(property_asset)
        return property_asset
    
    except Exception as e:
        print("UPDATE PROPERTY ASSET ERROR:", repr(e))
        raise HTTPException(status_code=400, detail="Unable to update property asset")
