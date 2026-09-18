from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.ticket_event import TicketEvent


def record_tool_action(
    db: Session,
    ticket: Ticket,
    *,
    tool: str,
    action: str,
    changed: bool,
    before: dict[str, object],
    after: dict[str, object],
    message: str,
) -> None:
    event = TicketEvent(
        ticket_id=ticket.id,
        event_type="TOOL_ACTION",
        actor="TECHNICIAN",
        details=message,
        event_data={
            "tool": tool,
            "action": action,
            "changed": changed,
            "before": before,
            "after": after,
        },
    )

    db.add(event)
