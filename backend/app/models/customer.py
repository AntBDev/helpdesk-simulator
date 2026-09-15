from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.user_account import UserAccount

if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.ticket import Ticket


class Customer(Base):
    __tablename__ = "customers"

    __table_args__ = (
        CheckConstraint(
            "technical_skill BETWEEN 1 AND 10",
            name="ck_customers_technical_skill",
        ),
        CheckConstraint(
            "patience BETWEEN 1 AND 10",
            name="ck_customers_patience",
        ),
        CheckConstraint(
            "cooperation BETWEEN 1 AND 10",
            name="ck_customers_cooperation",
        ),
        CheckConstraint(
            "confidence BETWEEN 1 AND 10",
            name="ck_customers_confidence",
        ),
        CheckConstraint(
            "communication_clarity BETWEEN 1 AND 10",
            name="ck_customers_communication_clarity",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    job_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    technical_skill: Mapped[int] = mapped_column(
        default=5,
        nullable=False,
    )

    patience: Mapped[int] = mapped_column(
        default=5,
        nullable=False,
    )

    cooperation: Mapped[int] = mapped_column(
        default=5,
        nullable=False,
    )

    confidence: Mapped[int] = mapped_column(
        default=5,
        nullable=False,
    )

    communication_clarity: Mapped[int] = mapped_column(
        default=5,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    devices: Mapped[list[Device]] = relationship(
        back_populates="customer",
    )

    tickets: Mapped[list[Ticket]] = relationship(
        back_populates="customer",
    )

    account: Mapped[UserAccount | None] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
        uselist=False,
    )
