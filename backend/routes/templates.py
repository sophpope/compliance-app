from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, or_
from uuid import UUID


import models

from db_utils import SessionDep
from auth_utils import CurrentProfileDep

router = APIRouter()


# Checklist Template Endpoints
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

@router.get('/templates', response_model=list[models.ChecklistTemplatePublic])
def get_templates(current_profile: CurrentProfileDep, session: SessionDep):
    try:
        templates = session.exec(
            select(models.ChecklistTemplates)
            .where(
                or_(
                models.ChecklistTemplates.account_id == current_profile.account_id,
                models.ChecklistTemplates.visibility == 'public',
                models.ChecklistTemplates.is_default.is_(True)
            ),
            models.ChecklistTemplates.is_active.is_(True)
        )).all()
        return templates
    except Exception as e:
        print("GET TEMPLATES ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Unable to retrieve templates")
    
@router.get('/template/{template_id}', response_model=models.ChecklistTemplatePublic)
def get_template(template_id: UUID, current_profile: CurrentProfileDep, session: SessionDep):
    try:
        template = session.exec(
            select(models.ChecklistTemplates)
            .where(
                models.ChecklistTemplates.id == template_id,
                or_(models.ChecklistTemplates.account_id == current_profile.account_id, 
                    models.ChecklistTemplates.visibility == 'public', 
                    models.ChecklistTemplates.is_default == True
                ),
                models.ChecklistTemplates.is_active == True
            )
        ).first()
        
        if template is None:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return template
    except Exception as e:
        print("GET TEMPLATE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Unable to retrieve template")

@router.patch("/template/{template_id}", response_model=models.ChecklistTemplatePublic)
def update_template(
    template_id: UUID, 
    template_data: models.ChecklistTemplateUpdate, 
    current_profile: CurrentProfileDep, 
    session: SessionDep
):
    try:
        template = session.exec(
            select(models.ChecklistTemplates)
            .where(
                models.ChecklistTemplates.id == template_id,
                models.ChecklistTemplates.account_id == current_profile.account_id
            )
        ).first()
        
        if template is None:
            raise HTTPException(status_code=404, detail="Template not found")
        
        update_data = template_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(template, key, value)

        session.add(template)
        session.commit()
        session.refresh(template)

        return template
    
    except Exception as e:
        print("UPDATE TEMPLATE ERROR:", repr(e))
        raise HTTPException(status_code=400, detail="Unable to update template")

