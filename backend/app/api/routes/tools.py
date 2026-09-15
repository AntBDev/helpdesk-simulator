from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.user_account import UserAccount
from app.schemas.account import AccountToolResult
from app.services.account_service import (
    get_account_by_customer_id,
    lookup_account,
    reset_mfa,
    reset_password,
    unlock_account,
)
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
