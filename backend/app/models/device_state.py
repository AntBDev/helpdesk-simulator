from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.device import Device


class DeviceState(Base):
    __tablename__ = "device_states"

    __table_args__ = (
        CheckConstraint(
            "cpu_usage_percent BETWEEN 0 AND 100",
            name="ck_device_states_cpu_usage",
        ),
        CheckConstraint(
            "memory_usage_percent BETWEEN 0 AND 100",
            name="ck_device_states_memory_usage",
        ),
        CheckConstraint(
            "disk_total_gb > 0",
            name="ck_device_states_disk_total",
        ),
        CheckConstraint(
            "disk_free_gb >= 0",
            name="ck_device_states_disk_free",
        ),
        CheckConstraint(
            "disk_free_gb <= disk_total_gb",
            name="ck_device_states_disk_capacity",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    device_id: Mapped[int] = mapped_column(
        ForeignKey(
            "devices.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    network_adapter_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    gateway_reachable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    dns_resolving: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    internet_reachable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    disk_total_gb: Mapped[int] = mapped_column(
        Integer,
        default=512,
        nullable=False,
    )

    disk_free_gb: Mapped[int] = mapped_column(
        Integer,
        default=256,
        nullable=False,
    )

    cpu_usage_percent: Mapped[int] = mapped_column(
        Integer,
        default=15,
        nullable=False,
    )

    memory_usage_percent: Mapped[int] = mapped_column(
        Integer,
        default=40,
        nullable=False,
    )

    pending_reboot: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    primary_service_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    primary_service_running: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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

    device: Mapped[Device] = relationship(
        back_populates="simulated_state",
    )
