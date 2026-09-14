from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceCreate


def get_devices(db: Session) -> list[Device]:
    statement = select(Device).order_by(Device.id)

    return list(db.scalars(statement).all())


def get_device_by_id(
    db: Session,
    device_id: int,
) -> Device | None:
    return db.get(Device, device_id)


def get_device_by_asset_tag(
    db: Session,
    asset_tag: str,
) -> Device | None:
    statement = select(Device).where(Device.asset_tag == asset_tag)

    return db.scalar(statement)


def get_device_by_hostname(
    db: Session,
    hostname: str,
) -> Device | None:
    statement = select(Device).where(Device.hostname == hostname)

    return db.scalar(statement)


def create_device(
    db: Session,
    device_data: DeviceCreate,
) -> Device:
    device = Device(**device_data.model_dump())

    db.add(device)
    db.commit()
    db.refresh(device)

    return device
