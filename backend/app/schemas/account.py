from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    customer_id: int
    username: str

    is_enabled: bool = True
    is_locked: bool = False
    failed_login_attempts: int = 0

    mfa_enrolled: bool = True
    password_reset_required: bool = False
    password_version: int = 1


class AccountRead(BaseModel):
    id: int
    customer_id: int
    username: str

    is_enabled: bool
    is_locked: bool
    failed_login_attempts: int

    mfa_enrolled: bool
    password_reset_required: bool
    password_version: int

    last_password_reset_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class AccountToolResult(BaseModel):
    action: str
    changed: bool
    message: str
    account: AccountRead
