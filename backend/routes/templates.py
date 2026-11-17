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

# Template Version Endpoints

@router.get('/template_versions/{template_id}', response_model=list[models.TemplateVersionPublic])
def get_template_version(template_id: UUID, current_profile: CurrentProfileDep, session: SessionDep):
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
        
        versions = session.exec(
            select(models.TemplateVersions)
            .where(
                models.TemplateVersions.template_id == template_id,
                models.ChecklistTemplates.is_active == True
            )
        ).all()
        
        return versions
    except Exception as e:
        print("GET TEMPLATE VERSIONS ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Unable to retrieve template versions")
    

@router.post('/add_template_version/{template_id}', response_model=models.TemplateVersionPublic)
def add_template_version(version_data: models.TemplateVersionCreate, 
                         template_id: UUID,
                         current_profile: CurrentProfileDep, 
                         session: SessionDep):
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
        
        version = models.TemplateVersions(
            **version_data.model_dump(), 
            template_id=template_id,
            created_by=current_profile.id
        )
        
        session.add(version)
        session.commit()
        session.refresh(version)
        return version
    except Exception as e:
        session.rollback()
        print("ADD TEMPLATE VERSION ERROR:")
        print(repr(e))
        raise

@router.patch("/template_version/{version_id}", response_model=models.TemplateVersionPublic)
def update_template_version(
    version_id: UUID, 
    version_data: models.TemplateVersionUpdate, 
    current_profile: CurrentProfileDep, 
    session: SessionDep
):
    try:
        version = session.exec(
            select(models.TemplateVersions)
            .where(
                models.TemplateVersions.id == version_id,
                models.ChecklistTemplates.account_id == current_profile.account_id
            )
        ).first()
        
        if version is None:
            raise HTTPException(status_code=404, detail="Template version not found")
        
        update_data = version_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(version, key, value)

        session.add(version)
        session.commit()
        session.refresh(version)

        return version
    
    except Exception as e:
        print("UPDATE TEMPLATE VERSION ERROR:", repr(e))
        raise HTTPException(status_code=400, detail="Unable to update template version")
    
@router.get('/templates/{template_id}/versions', response_model=list[models.TemplateVersionPublic])
def get_template_versions(template_id: UUID, current_profile: CurrentProfileDep, session: SessionDep):
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
        
        versions = session.exec(
            select(models.TemplateVersions)
            .where(
                models.TemplateVersions.template_id == template_id,
                models.ChecklistTemplates.is_active == True
            )
        ).all()
        
        return versions
    except Exception as e:
        print("GET TEMPLATE VERSIONS ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Unable to retrieve template versions")
    