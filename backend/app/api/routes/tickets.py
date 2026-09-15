from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ticket import (
    TicketCreate,
    TicketEventRead,
    TicketRead,
    TicketStatusUpdate,
)
from app.services.customer_service import get_customer_by_id
from app.services.device_service import get_device_by_id
from app.services.ticket_service import (
    create_ticket,
    get_ticket_by_number,
    get_ticket_events,
    get_tickets,
    update_ticket_status,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


DbSession = Annotated[Session, Depends(get_db)]


@router.get(
    "",
    response_model=list[TicketRead],
)
def list_tickets(
    db: DbSession,
) -> list[TicketRead]:
    return get_tickets(db)


@router.post(
    "",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
)
def add_ticket(
    ticket_data: TicketCreate,
    db: DbSession,
) -> TicketRead:

    customer = get_customer_by_id(
        db,
        ticket_data.customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    if ticket_data.device_id is not None:
        device = get_device_by_id(
            db,
            ticket_data.device_id,
        )

        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )

        if (
            device.customer_id is not None
            and device.customer_id != ticket_data.customer_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=("The selected device is assigned to a different customer"),
            )

    return create_ticket(
        db,
        ticket_data,
    )


@router.get(
    "/{ticket_number}",
    response_model=TicketRead,
)
def retrieve_ticket(
    ticket_number: str,
    db: DbSession,
) -> TicketRead:

    ticket = get_ticket_by_number(
        db,
        ticket_number,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket


@router.get(
    "/{ticket_number}/events",
    response_model=list[TicketEventRead],
)
def retrieve_ticket_events(
    ticket_number: str,
    db: DbSession,
) -> list[TicketEventRead]:

    ticket = get_ticket_by_number(
        db,
        ticket_number,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return get_ticket_events(
        db,
        ticket.id,
    )


@router.patch(
    "/{ticket_number}/status",
    response_model=TicketRead,
)
def change_ticket_status(
    ticket_number: str,
    status_data: TicketStatusUpdate,
    db: DbSession,
) -> TicketRead:
    ticket = get_ticket_by_number(
        db,
        ticket_number,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    try:
        return update_ticket_status(
            db,
            ticket,
            status_data.status,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error
