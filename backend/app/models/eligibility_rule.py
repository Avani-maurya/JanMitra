from typing import Any,Literal

from pydantic import BaseModel, Field


class EligibilityCondition(BaseModel):
    field: str
    operator: Literal[
        "==",
        "!=",
        ">=",
        ">",
        "<",
        "<=",
        "in",
        "not_in"
    ]
    value: Any


class EligibilityRule(BaseModel):
    id: str
    scheme_id: str
    conditions: list[EligibilityCondition] = Field(min_length=1)
    logic: Literal["AND","OR"] ="AND"