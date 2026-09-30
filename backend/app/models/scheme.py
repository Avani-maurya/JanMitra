from datetime import datetime

from pydantic import BaseModel, Field


class Scheme(BaseModel):
    id: str
    name: str = Field(min_length=1)
    description: str
    ministry: str | None = None
    category: str
    level: str
    state: str | None = None
    benefits: list[str] = Field(default_factory=list)
    application_url: str | None = None
    official_source: str | None = None
    documents_required: list[str] = Field(default_factory=list)
    eligibility_rule_id: str
    status: str = "active"
    last_verified: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)