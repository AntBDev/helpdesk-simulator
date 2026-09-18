from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.device import Device
from app.models.device_state import DeviceState
from app.models.ticket import Ticket
from app.models.user_account import UserAccount
from app.schemas.account import AccountToolResult
from app.schemas.device_state import DeviceToolResult
from app.services.account_service import (
    get_account_by_customer_id,
    lookup_account,
    reset_mfa,
    reset_password,
    unlock_account,
)
from app.services.device_diagnostic_service import (
    check_resources,
    enable_network_adapter,
    get_device_state_by_device_id,
    inspect_device,
    reboot_device,
    restart_primary_service,
    test_connectivity,
    test_dns,
)
from app.services.device_service import get_device_by_id
from app.services.ticket_service import (
    get_ticket_by_number,
)

router = APIRouter(
    prefix="/tickets/{ticket_number}/tools",
    tags=["Simulation Tools"],
)


DbSession = Annotated[
    Session,
    Depends(get_db),
]


def get_ticket_account(
    db: Session,
    ticket_number: str,
) -> tuple[Ticket, UserAccount]:
    ticket = get_ticket_by_number(
        db,
        ticket_number,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    account = get_account_by_customer_id(
        db,
        ticket.customer_id,
    )

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Customer does not have a simulated user account"),
        )

    return ticket, account


@router.post(
    "/account/lookup",
    response_model=AccountToolResult,
)
def account_lookup(
    ticket_number: str,
    db: DbSession,
) -> AccountToolResult:
    ticket, account = get_ticket_account(
        db,
        ticket_number,
    )

    account, changed, message = lookup_account(
        db,
        ticket,
        account,
    )

    return AccountToolResult(
        action="LOOKUP",
        changed=changed,
        message=message,
        account=account,
    )


@router.post(
    "/account/unlock",
    response_model=AccountToolResult,
)
def account_unlock(
    ticket_number: str,
    db: DbSession,
) -> AccountToolResult:
    ticket, account = get_ticket_account(
        db,
        ticket_number,
    )

    account, changed, message = unlock_account(
        db,
        ticket,
        account,
    )

    return AccountToolResult(
        action="UNLOCK",
        changed=changed,
        message=message,
        account=account,
    )


@router.post(
    "/account/password-reset",
    response_model=AccountToolResult,
)
def account_password_reset(
    ticket_number: str,
    db: DbSession,
) -> AccountToolResult:
    ticket, account = get_ticket_account(
        db,
        ticket_number,
    )

    account, changed, message = reset_password(
        db,
        ticket,
        account,
    )

    return AccountToolResult(
        action="PASSWORD_RESET",
        changed=changed,
        message=message,
        account=account,
    )


@router.post(
    "/account/mfa-reset",
    response_model=AccountToolResult,
)
def account_mfa_reset(
    ticket_number: str,
    db: DbSession,
) -> AccountToolResult:
    ticket, account = get_ticket_account(
        db,
        ticket_number,
    )

    account, changed, message = reset_mfa(
        db,
        ticket,
        account,
    )

    return AccountToolResult(
        action="MFA_RESET",
        changed=changed,
        message=message,
        account=account,
    )


def get_ticket_device_state(
    db: Session,
    ticket_number: str,
) -> tuple[
    Ticket,
    Device,
    DeviceState,
]:
    ticket = get_ticket_by_number(
        db,
        ticket_number,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    if ticket.device_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Ticket has no associated device"),
        )

    device = get_device_by_id(
        db,
        ticket.device_id,
    )

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found",
        )

    device_state = get_device_state_by_device_id(
        db,
        device.id,
    )

    if device_state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=("Device does not have simulated diagnostic state"),
        )

    return ticket, device, device_state


@router.post(
    "/device/inspect",
    response_model=DeviceToolResult,
)
def device_inspect(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = inspect_device(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="INSPECT",
        changed=changed,
        message=message,
        state=state,
    )


@router.post(
    "/device/connectivity-test",
    response_model=DeviceToolResult,
)
def device_connectivity_test(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = test_connectivity(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="CONNECTIVITY_TEST",
        changed=changed,
        message=message,
        state=state,
    )


@router.post(
    "/device/dns-test",
    response_model=DeviceToolResult,
)
def device_dns_test(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = test_dns(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="DNS_TEST",
        changed=changed,
        message=message,
        state=state,
    )


@router.post(
    "/device/resource-check",
    response_model=DeviceToolResult,
)
def device_resource_check(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = check_resources(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="RESOURCE_CHECK",
        changed=changed,
        message=message,
        state=state,
    )


@router.post(
    "/device/enable-network-adapter",
    response_model=DeviceToolResult,
)
def device_enable_network_adapter(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = enable_network_adapter(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="ENABLE_NETWORK_ADAPTER",
        changed=changed,
        message=message,
        state=state,
    )


@router.post(
    "/device/restart-service",
    response_model=DeviceToolResult,
)
def device_restart_service(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = restart_primary_service(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="RESTART_SERVICE",
        changed=changed,
        message=message,
        state=state,
    )


@router.post(
    "/device/reboot",
    response_model=DeviceToolResult,
)
def device_reboot(
    ticket_number: str,
    db: DbSession,
) -> DeviceToolResult:
    ticket, _, state = get_ticket_device_state(
        db,
        ticket_number,
    )

    state, changed, message = reboot_device(
        db,
        ticket,
        state,
    )

    return DeviceToolResult(
        action="REBOOT",
        changed=changed,
        message=message,
        state=state,
    )
