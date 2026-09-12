from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DeviceStatus, DeviceType

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.ticket import Ticket


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)

    asset_tag: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    hostname: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "customers.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    device_type: Mapped[DeviceType] = mapped_column(
        SAEnum(
            DeviceType,
            name="device_type",
        ),
        nullable=False,
    )

    status: Mapped[DeviceStatus] = mapped_column(
        SAEnum(
            DeviceStatus,
            name="device_status",
        ),
        default=DeviceStatus.ONLINE,
        nullable=False,
    )

    manufacturer: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    operating_system: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    os_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    customer: Mapped["Customer | None"] = relationship(
        back_populates="devices",
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="device",
    )