from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import DeviceStatus, DeviceType


class DeviceBase(BaseModel):
    asset_tag: str = Field(min_length=1, max_length=50)
    hostname: str = Field(min_length=1, max_length=100)

    customer_id: int | None = None

    device_type: DeviceType
    status: DeviceStatus = DeviceStatus.ONLINE

    manufacturer: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=150)

    operating_system: str = Field(min_length=1, max_length=100)
    os_version: str | None = Field(default=None, max_length=100)

    ip_address: str | None = Field(default=None, max_length=45)


class DeviceCreate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
