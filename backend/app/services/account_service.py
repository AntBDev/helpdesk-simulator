from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user_account import UserAccount
from app.schemas.account import AccountCreate
from app.services.tool_event_service import record_tool_action


def get_account_by_customer_id(
    db: Session,
    customer_id: int,
) -> UserAccount | None:
    statement = select(UserAccount).where(UserAccount.customer_id == customer_id)

    return db.scalar(statement)


def create_account(
    db: Session,
    account_data: AccountCreate,
) -> UserAccount:
    account = UserAccount(**account_data.model_dump())

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def account_snapshot(
    account: UserAccount,
) -> dict[str, object]:
    return {
        "username": account.username,
        "is_enabled": account.is_enabled,
        "is_locked": account.is_locked,
        "failed_login_attempts": (account.failed_login_attempts),
        "mfa_enrolled": account.mfa_enrolled,
        "password_reset_required": (account.password_reset_required),
        "password_version": (account.password_version),
    }


def lookup_account(
    db: Session,
    ticket: Ticket,
    account: UserAccount,
) -> tuple[UserAccount, bool, str]:
    state = account_snapshot(account)

    message = f"Technician looked up account {account.username}."

    try:
        record_tool_action(
            db,
            ticket,
            tool="ACCOUNT_ADMIN",
            action="LOOKUP",
            changed=False,
            before=state,
            after=state,
            message=message,
        )

        db.commit()
        db.refresh(account)

        return account, False, message

    except Exception:
        db.rollback()
        raise


def unlock_account(
    db: Session,
    ticket: Ticket,
    account: UserAccount,
) -> tuple[UserAccount, bool, str]:
    before = account_snapshot(account)

    changed = account.is_locked

    if account.is_locked:
        account.is_locked = False
        account.failed_login_attempts = 0

        message = f"Account {account.username} was unlocked."
    else:
        message = f"Account {account.username} was already unlocked."

    after = account_snapshot(account)

    try:
        record_tool_action(
            db,
            ticket,
            tool="ACCOUNT_ADMIN",
            action="UNLOCK",
            changed=changed,
            before=before,
            after=after,
            message=message,
        )

        db.commit()
        db.refresh(account)

        return account, changed, message

    except Exception:
        db.rollback()
        raise


def reset_password(
    db: Session,
    ticket: Ticket,
    account: UserAccount,
) -> tuple[UserAccount, bool, str]:
    before = account_snapshot(account)

    account.password_version += 1
    account.password_reset_required = True
    account.failed_login_attempts = 0
    account.last_password_reset_at = datetime.now(UTC)

    after = account_snapshot(account)

    message = f"Password reset completed for {account.username}."

    try:
        record_tool_action(
            db,
            ticket,
            tool="ACCOUNT_ADMIN",
            action="PASSWORD_RESET",
            changed=True,
            before=before,
            after=after,
            message=message,
        )

        db.commit()
        db.refresh(account)

        return account, True, message

    except Exception:
        db.rollback()
        raise


def reset_mfa(
    db: Session,
    ticket: Ticket,
    account: UserAccount,
) -> tuple[UserAccount, bool, str]:
    before = account_snapshot(account)

    changed = account.mfa_enrolled

    account.mfa_enrolled = False

    after = account_snapshot(account)

    if changed:
        message = f"MFA enrollment for {account.username} was reset."
    else:
        message = f"Account {account.username} had no active MFA enrollment."

    try:
        record_tool_action(
            db,
            ticket,
            tool="ACCOUNT_ADMIN",
            action="MFA_RESET",
            changed=changed,
            before=before,
            after=after,
            message=message,
        )

        db.commit()
        db.refresh(account)

        return account, changed, message

    except Exception:
        db.rollback()
        raise
