from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import TicketPriority, TicketStatus

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.device import Device
    from app.models.ticket_event import TicketEvent


class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__ = (
        Index(
            "ix_tickets_status_priority",
            "status",
            "priority",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    ticket_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SAEnum(
            TicketPriority,
            name="ticket_priority",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(
            TicketStatus,
            name="ticket_status",
        ),
        default=TicketStatus.NEW,
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    subcategory: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    device_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "devices.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    sla_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="tickets",
    )

    device: Mapped["Device | None"] = relationship(
        back_populates="tickets",
    )

    events: Mapped[list["TicketEvent"]] = relationship(
        back_populates="ticket",
        cascade="all, delete-orphan",
    )