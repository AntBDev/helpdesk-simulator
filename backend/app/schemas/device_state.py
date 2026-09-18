from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class DeviceStateCreate(BaseModel):
    device_id: int

    network_adapter_enabled: bool = True
    gateway_reachable: bool = True
    dns_resolving: bool = True
    internet_reachable: bool = True

    disk_total_gb: int = Field(
        default=512,
        gt=0,
    )

    disk_free_gb: int = Field(
        default=256,
        ge=0,
    )

    cpu_usage_percent: int = Field(
        default=15,
        ge=0,
        le=100,
    )

    memory_usage_percent: int = Field(
        default=40,
        ge=0,
        le=100,
    )

    pending_reboot: bool = False

    primary_service_name: str | None = None
    primary_service_running: bool = True


class DeviceStateRead(DeviceStateCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DeviceToolResult(BaseModel):
    action: str
    changed: bool
    message: str
    state: DeviceStateRead
