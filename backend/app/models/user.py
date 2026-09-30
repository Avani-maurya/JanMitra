from datetime import datetime, timezone

from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)

    gender: str | None = None

    state: str
    district: str | None = None

    annual_income: float | None = Field(default=None, ge=0)
    occupation: str | None = None
    category: str | None = None
    education_level: str | None = None
    marital_status: str | None = None

    is_disabled: bool = False
    disability_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100
    )

    is_farmer: bool = False
    landholding_status: bool | None = None

    is_student: bool = False
    school_class: int | None = Field(default=None, ge=1, le=12)

    is_urban: bool | None = None
    owns_pucca_house: bool | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )