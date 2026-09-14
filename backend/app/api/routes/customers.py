from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerRead
from app.services.customer_service import (
    create_customer,
    get_customer_by_email,
    get_customer_by_id,
    get_customers,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=list[CustomerRead],
)
def list_customers(
    db: DbSession,
) -> list[CustomerRead]:
    return get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerRead,
)
def retrieve_customer(
    customer_id: int,
    db: DbSession,
) -> CustomerRead:
    customer = get_customer_by_id(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
)
def add_customer(
    customer_data: CustomerCreate,
    db: DbSession,
) -> CustomerRead:
    existing_customer = get_customer_by_email(
        db,
        str(customer_data.email),
    )

    if existing_customer is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A customer with this email already exists",
        )

    return create_customer(
        db,
        customer_data,
    )
