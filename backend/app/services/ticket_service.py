from datetime import UTC, datetime, timedelta

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.enums import TicketPriority, TicketStatus
from app.models.ticket import Ticket
from app.models.ticket_event import TicketEvent
from app.schemas.ticket import TicketCreate

SLA_HOURS = {
    TicketPriority.HIGH: 2,
    TicketPriority.MEDIUM: 8,
    TicketPriority.LOW: 24,
}


def get_tickets(
    db: Session,
) -> list[Ticket]:
    statement = (
        select(Ticket)
        .order_by(Ticket.created_at.desc())
    )

    return list(
        db.scalars(statement).all()
    )


def get_ticket_by_number(
    db: Session,
    ticket_number: str,
) -> Ticket | None:
    statement = select(Ticket).where(
        Ticket.ticket_number == ticket_number.upper()
    )

    return db.scalar(statement)


def get_ticket_events(
    db: Session,
    ticket_id: int,
) -> list[TicketEvent]:
    statement = (
        select(TicketEvent)
        .where(TicketEvent.ticket_id == ticket_id)
        .order_by(TicketEvent.created_at)
    )

    return list(
        db.scalars(statement).all()
    )


def generate_ticket_number(
    db: Session,
) -> str:
    sequence_value = db.scalar(
        text(
            "SELECT nextval('ticket_number_seq')"
        )
    )

    if sequence_value is None:
        raise RuntimeError(
            "Unable to generate ticket number"
        )

    return f"INC-{sequence_value:06d}"


def calculate_sla_deadline(
    priority: TicketPriority,
) -> datetime:
    current_time = datetime.now(UTC)

    return current_time + timedelta(
        hours=SLA_HOURS[priority]
    )


def create_ticket(
    db: Session,
    ticket_data: TicketCreate,
) -> Ticket:
    ticket_number = generate_ticket_number(db)

    sla_deadline = calculate_sla_deadline(
        ticket_data.priority
    )

    ticket = Ticket(
        ticket_number=ticket_number,
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        status=TicketStatus.NEW,
        category=ticket_data.category,
        subcategory=ticket_data.subcategory,
        customer_id=ticket_data.customer_id,
        device_id=ticket_data.device_id,
        sla_deadline=sla_deadline,
    )

    try:
        db.add(ticket)

        # We need the database-generated ticket ID
        # before creating its audit event.
        db.flush()

        event = TicketEvent(
            ticket_id=ticket.id,
            event_type="TICKET_CREATED",
            actor="SYSTEM",
            details=f"Ticket {ticket.ticket_number} created.",
            event_data={
                "ticket_number": ticket.ticket_number,
                "priority": ticket.priority.value,
                "status": ticket.status.value,
                "customer_id": ticket.customer_id,
                "device_id": ticket.device_id,
                "sla_deadline": (
                    ticket.sla_deadline.isoformat()
                    if ticket.sla_deadline
                    else None
                ),
            },
        )

        db.add(event)

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise