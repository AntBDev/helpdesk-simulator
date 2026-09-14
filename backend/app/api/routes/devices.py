from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.device import DeviceCreate, DeviceRead
from app.services.customer_service import get_customer_by_id
from app.services.device_service import (
    create_device,
    get_device_by_asset_tag,
    get_device_by_hostname,
    get_device_by_id,
    get_devices,
)


router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=list[DeviceRead],
)
def list_devices(
    db: DbSession,
) -> list[DeviceRead]:
    return get_devices(db)


@router.get(
    "/{device_id}",
    response_model=DeviceRead,
)
def retrieve_device(
    device_id: int,
    db: DbSession,
) -> DeviceRead:
    device = get_device_by_id(
        db,
        device_id,
    )

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    return device


@router.post(
    "",
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
)
def add_device(
    device_data: DeviceCreate,
    db: DbSession,
) -> DeviceRead:

    if device_data.customer_id is not None:
        customer = get_customer_by_id(
            db,
            device_data.customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

    existing_asset = get_device_by_asset_tag(
        db,
        device_data.asset_tag,
    )

    if existing_asset is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A device with this asset tag already exists",
        )

    existing_hostname = get_device_by_hostname(
        db,
        device_data.hostname,
    )

    if existing_hostname is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A device with this hostname already exists",
        )

    return create_device(
        db,
        device_data,
    )