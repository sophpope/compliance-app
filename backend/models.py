from uuid import UUID
from datetime import datetime

from sqlmodel import SQLModel, Field

class Accounts(SQLModel, table=True):
    __tablename__ = "accounts"

    id: UUID = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Profiles(SQLModel, table=True):
    __tablename__ = "profiles"

    id: UUID = Field(default=None, primary_key=True)
    account_id: UUID = Field(foreign_key="accounts.id", nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    role: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Properties(SQLModel, table=True):
    __tablename__ = "properties"

    id: UUID = Field(default=None, primary_key=True)
    account_id: UUID = Field(foreign_key="accounts.id", nullable=False)
    property_name: str = Field(nullable=False)
    address_1: str = Field(nullable=False)
    address_2: str = Field(nullable=True)
    city: str = Field(nullable=False)
    county: str = Field(nullable=False)
    postcode: str = Field(nullable=False)
    description: str = Field(nullable=True)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class ChecklistTemplates(SQLModel, table=True):
    __tablename__ = "checklist_templates"

    id: UUID = Field(default=None, primary_key=True)
    account_id: UUID = Field(foreign_key="accounts.id", nullable=True)
    checklist_name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    is_default: bool = Field(default=False, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TemplateVersions(SQLModel, table=True):
    __tablename__ = "template_versions"

    id: UUID = Field(default=None, primary_key=True)
    template_id: UUID = Field(foreign_key="checklist_templates.id", nullable=False)
    version_number: int = Field(nullable=False)
    status: str = Field(nullable=False)
    template_data: str = Field(nullable=False)  # JSONB data as string
    created_by: UUID = Field(foreign_key="profiles.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class PropertyAssets(SQLModel, table=True):
    __tablename__ = "property_assets"

    id: UUID = Field(default=None, primary_key=True)
    property_id: UUID = Field(foreign_key="properties.id", nullable=False)
    asset_name: str = Field(nullable=False)
    asset_type: str = Field(nullable=False)
    asset_variation: str = Field(nullable=False)
    location: str = Field(nullable=False)
    description: str = Field(nullable=True)
    expiry_date: datetime = Field(nullable=True)
    installation_date: datetime = Field(nullable=True)
    last_service_date: datetime = Field(nullable=True)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class PropertyChecklists(SQLModel, table=True):
    __tablename__ = "property_checklists"

    id: UUID = Field(default=None, primary_key=True)
    property_id: UUID = Field(foreign_key="properties.id", nullable=False)
    template_version_id: UUID = Field(foreign_key="template_versions.id", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Checks(SQLModel, table=True):
    __tablename__ = "checks"

    id: UUID = Field(default=None, primary_key=True)
    property_checklist_id: UUID = Field(foreign_key="property_checklists.id", nullable=False)
    submitted_by: UUID = Field(foreign_key="profiles.id", nullable=True)
    submitted_at: datetime = Field(nullable=True)
    status: str = Field(nullable=False)

class CheckResponses(SQLModel, table=True):
    __tablename__ = "check_responses"

    id: UUID = Field(default=None, primary_key=True)
    check_id: UUID = Field(foreign_key="checks.id", nullable=False)
    item_id: str = Field(nullable=False)
    asset_id: UUID = Field(foreign_key="property_assets.id", nullable=True)
    response_value: str = Field(nullable=False)
    notes: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# models for post requests - adding new data to the database 

class AccountCreate(SQLModel):
    name: str
    email: str

class ProfileCreate(SQLModel):
    account_id: UUID
    first_name: str
    last_name: str
    email: str
    role: str

class PropertyCreate(SQLModel):
    account_id: UUID 
    property_name: str
    address_1: str
    address_2: str | None = None
    city: str
    county: str
    postcode: str
    description: str | None = None

class ChecklistTemplateCreate(SQLModel):
    account_id: UUID 
    checklist_name: str
    description: str | None = None
    is_default: bool = False

class TemplateVersionCreate(SQLModel):
    template_id: UUID
    version_number: int
    status: str
    template_data: str  # JSONB data as string
    created_by: UUID

class PropertyAssetCreate(SQLModel):
    property_id: UUID
    asset_name: str
    asset_type: str
    asset_variation: str
    location: str
    description: str | None = None
    expiry_date: datetime | None = None
    installation_date: datetime | None = None
    last_service_date: datetime | None = None

class PropertyChecklistCreate(SQLModel):
    property_id: UUID
    template_version_id: UUID

class CheckCreate(SQLModel):
    property_checklist_id: UUID
    submitted_by: UUID | None = None
    status: str

class CheckResponseCreate(SQLModel):
    check_id: UUID
    item_id: str
    asset_id: UUID | None = None
    response_value: str
    notes: str | None = None

# Public Models 

