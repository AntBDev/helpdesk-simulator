from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)

    description: str = Field(
        min_length=1,
        max_length=5000,
    )

    priority: TicketPriority

    category: str = Field(
        min_length=1,
        max_length=100,
    )

    subcategory: str | None = Field(
        default=None,
        max_length=100,
    )

    customer_id: int
    device_id: int | None = None


class TicketRead(BaseModel):
    id: int
    ticket_number: str

    title: str
    description: str

    priority: TicketPriority
    status: TicketStatus

    category: str
    subcategory: str | None

    customer_id: int
    device_id: int | None

    sla_deadline: datetime | None
    resolved_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketEventRead(BaseModel):
    id: int
    ticket_id: int

    event_type: str
    actor: str

    details: str | None
    event_data: dict[str, Any]

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)