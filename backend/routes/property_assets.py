from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from uuid import UUID

import models

from db_utils import SessionDep
from auth_utils import CurrentProfileDep

router = APIRouter()

@router.get('/property_assets/{property_id}', response_model=list[models.PropertyAssetPublic])
def get_property_assets(property_id: UUID,
                        current_profile: CurrentProfileDep, 
                        session: SessionDep):
    try:
        property_assets = session.exec(
            select(models.PropertyAssets)
            .where(
                models.PropertyAssets.property_id == property_id,
                models.PropertyAssets.account_id == current_profile.account_id
            )
        ).all()
        return property_assets
    except Exception as e:
        return {"error": str(e)}