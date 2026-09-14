from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(min_length=1, max_length=100)
    job_title: str = Field(min_length=1, max_length=150)

    technical_skill: int = Field(default=5, ge=1, le=10)
    patience: int = Field(default=5, ge=1, le=10)
    cooperation: int = Field(default=5, ge=1, le=10)
    confidence: int = Field(default=5, ge=1, le=10)
    communication_clarity: int = Field(default=5, ge=1, le=10)


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
