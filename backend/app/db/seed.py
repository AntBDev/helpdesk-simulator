from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.enums import (
    DeviceStatus,
    DeviceType,
    TicketPriority,
)
from app.models.ticket import Ticket
from app.schemas.customer import CustomerCreate
from app.schemas.device import DeviceCreate
from app.schemas.ticket import TicketCreate
from app.services.customer_service import (
    create_customer,
    get_customer_by_email,
)
from app.services.device_service import (
    create_device,
    get_device_by_asset_tag,
    get_device_by_hostname,
)
from app.services.ticket_service import create_ticket

CUSTOMERS = [
    {
        "first_name": "Jessica",
        "last_name": "Turner",
        "email": "jessica.turner@example.com",
        "department": "Accounting",
        "job_title": "Payroll Specialist",
        "technical_skill": 3,
        "patience": 5,
        "cooperation": 8,
        "confidence": 7,
        "communication_clarity": 6,
    },
    {
        "first_name": "Marcus",
        "last_name": "Reed",
        "email": "marcus.reed@example.com",
        "department": "Finance",
        "job_title": "Senior Financial Analyst",
        "technical_skill": 7,
        "patience": 6,
        "cooperation": 8,
        "confidence": 8,
        "communication_clarity": 8,
    },
    {
        "first_name": "Olivia",
        "last_name": "Bennett",
        "email": "olivia.bennett@example.com",
        "department": "Human Resources",
        "job_title": "HR Coordinator",
        "technical_skill": 2,
        "patience": 8,
        "cooperation": 9,
        "confidence": 4,
        "communication_clarity": 7,
    },
    {
        "first_name": "Ethan",
        "last_name": "Cole",
        "email": "ethan.cole@example.com",
        "department": "Sales",
        "job_title": "Account Executive",
        "technical_skill": 3,
        "patience": 2,
        "cooperation": 4,
        "confidence": 9,
        "communication_clarity": 5,
    },
    {
        "first_name": "Maya",
        "last_name": "Brooks",
        "email": "maya.brooks@example.com",
        "department": "Engineering",
        "job_title": "Software Engineer",
        "technical_skill": 9,
        "patience": 7,
        "cooperation": 9,
        "confidence": 8,
        "communication_clarity": 9,
    },
    {
        "first_name": "Noah",
        "last_name": "Price",
        "email": "noah.price@example.com",
        "department": "Operations",
        "job_title": "Operations Coordinator",
        "technical_skill": 5,
        "patience": 7,
        "cooperation": 8,
        "confidence": 5,
        "communication_clarity": 8,
    },
    {
        "first_name": "Chloe",
        "last_name": "Morgan",
        "email": "chloe.morgan@example.com",
        "department": "Marketing",
        "job_title": "Marketing Specialist",
        "technical_skill": 6,
        "patience": 5,
        "cooperation": 7,
        "confidence": 6,
        "communication_clarity": 8,
    },
    {
        "first_name": "Derrick",
        "last_name": "Hayes",
        "email": "derrick.hayes@example.com",
        "department": "Sales",
        "job_title": "Regional Sales Manager",
        "technical_skill": 2,
        "patience": 2,
        "cooperation": 3,
        "confidence": 10,
        "communication_clarity": 5,
    },
    {
        "first_name": "Sophia",
        "last_name": "Kim",
        "email": "sophia.kim@example.com",
        "department": "Legal",
        "job_title": "Legal Assistant",
        "technical_skill": 4,
        "patience": 8,
        "cooperation": 9,
        "confidence": 5,
        "communication_clarity": 9,
    },
    {
        "first_name": "Andre",
        "last_name": "Miller",
        "email": "andre.miller@example.com",
        "department": "Operations",
        "job_title": "Warehouse Supervisor",
        "technical_skill": 2,
        "patience": 4,
        "cooperation": 7,
        "confidence": 7,
        "communication_clarity": 4,
    },
]


DEVICES = [
    {
        "customer_email": "jessica.turner@example.com",
        "asset_tag": "AST-000017",
        "hostname": "ACC-LT-017",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Dell",
        "model": "Latitude 5540",
        "operating_system": "Windows 11 Enterprise",
        "os_version": "24H2",
        "ip_address": "10.24.17.82",
    },
    {
        "customer_email": "marcus.reed@example.com",
        "asset_tag": "AST-000021",
        "hostname": "FIN-LT-021",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Lenovo",
        "model": "ThinkPad T14",
        "operating_system": "Windows 11 Enterprise",
        "os_version": "24H2",
        "ip_address": "10.24.21.41",
    },
    {
        "customer_email": "olivia.bennett@example.com",
        "asset_tag": "AST-000028",
        "hostname": "HR-LT-028",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Dell",
        "model": "Latitude 5450",
        "operating_system": "Windows 11 Enterprise",
        "os_version": "24H2",
        "ip_address": "10.24.28.33",
    },
    {
        "customer_email": "ethan.cole@example.com",
        "asset_tag": "AST-000034",
        "hostname": "SALES-LT-034",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "HP",
        "model": "EliteBook 840",
        "operating_system": "Windows 11 Enterprise",
        "os_version": "24H2",
        "ip_address": "10.24.34.71",
    },
    {
        "customer_email": "maya.brooks@example.com",
        "asset_tag": "AST-000041",
        "hostname": "ENG-LT-041",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Lenovo",
        "model": "ThinkPad P1",
        "operating_system": "Ubuntu Linux",
        "os_version": "26.04",
        "ip_address": "10.24.41.19",
    },
    {
        "customer_email": "noah.price@example.com",
        "asset_tag": "AST-000052",
        "hostname": "OPS-DT-052",
        "device_type": DeviceType.DESKTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Dell",
        "model": "OptiPlex 7020",
        "operating_system": "Windows 11 Enterprise",
        "os_version": "24H2",
        "ip_address": "10.24.52.22",
    },
    {
        "customer_email": "chloe.morgan@example.com",
        "asset_tag": "AST-000061",
        "hostname": "MKT-LT-061",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Apple",
        "model": "MacBook Pro",
        "operating_system": "macOS",
        "os_version": "15",
        "ip_address": "10.24.61.14",
    },
    {
        "customer_email": "derrick.hayes@example.com",
        "asset_tag": "AST-000072",
        "hostname": "SALES-LT-072",
        "device_type": DeviceType.LAPTOP,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Dell",
        "model": "Latitude 5550",
        "operating_system": "Windows 11 Enterprise",
        "os_version": "24H2",
        "ip_address": "10.24.72.57",
    },
    {
        "customer_email": None,
        "asset_tag": "AST-PRN-001",
        "hostname": "HQ-PRN-01",
        "device_type": DeviceType.PRINTER,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "HP",
        "model": "LaserJet Enterprise M611",
        "operating_system": "Embedded",
        "os_version": None,
        "ip_address": "10.24.100.20",
    },
    {
        "customer_email": None,
        "asset_tag": "AST-PRN-002",
        "hostname": "HQ-PRN-02",
        "device_type": DeviceType.PRINTER,
        "status": DeviceStatus.ONLINE,
        "manufacturer": "Canon",
        "model": "imageRUNNER DX",
        "operating_system": "Embedded",
        "os_version": None,
        "ip_address": "10.24.100.21",
    },
]


TICKETS = [
    {
        "customer_email": "jessica.turner@example.com",
        "device_hostname": "ACC-LT-017",
        "title": "Unable to access payroll",
        "description": (
            "Payroll application rejects the employee's login "
            "during payroll processing."
        ),
        "priority": TicketPriority.HIGH,
        "category": "Accounts",
        "subcategory": "Authentication",
    },
    {
        "customer_email": "marcus.reed@example.com",
        "device_hostname": "FIN-LT-021",
        "title": "VPN connects but internal sites do not load",
        "description": (
            "The VPN reports a successful connection, but internal "
            "company websites cannot be reached."
        ),
        "priority": TicketPriority.MEDIUM,
        "category": "Networking",
        "subcategory": "VPN",
    },
    {
        "customer_email": "olivia.bennett@example.com",
        "device_hostname": "HR-LT-028",
        "title": "Outlook repeatedly asks for password",
        "description": (
            "Outlook continues prompting for credentials even after "
            "the employee enters the correct password."
        ),
        "priority": TicketPriority.MEDIUM,
        "category": "Email",
        "subcategory": "Microsoft 365",
    },
    {
        "customer_email": "ethan.cole@example.com",
        "device_hostname": "SALES-LT-034",
        "title": "Second monitor not detected",
        "description": (
            "The external monitor connected through the docking station "
            "is no longer detected."
        ),
        "priority": TicketPriority.LOW,
        "category": "Hardware",
        "subcategory": "Display",
    },
    {
        "customer_email": "maya.brooks@example.com",
        "device_hostname": "ENG-LT-041",
        "title": "Cannot resolve internal development hostname",
        "description": (
            "The workstation can access the internet but cannot resolve "
            "an internal development server hostname."
        ),
        "priority": TicketPriority.MEDIUM,
        "category": "Networking",
        "subcategory": "DNS",
    },
    {
        "customer_email": "derrick.hayes@example.com",
        "device_hostname": "SALES-LT-072",
        "title": "Account locked before client presentation",
        "description": (
            "The employee cannot sign in after several failed password "
            "attempts and has an upcoming client presentation."
        ),
        "priority": TicketPriority.HIGH,
        "category": "Accounts",
        "subcategory": "Account Lockout",
    },
    {
        "customer_email": "noah.price@example.com",
        "device_hostname": "HQ-PRN-01",
        "title": "Shared printer shows offline",
        "description": (
            "Operations staff cannot print to the first-floor shared "
            "printer even though the printer appears powered on."
        ),
        "priority": TicketPriority.MEDIUM,
        "category": "Hardware",
        "subcategory": "Printer",
    },
    {
        "customer_email": "chloe.morgan@example.com",
        "device_hostname": None,
        "title": "Unexpected MFA approval requests",
        "description": (
            "The employee received several MFA approval prompts that "
            "they did not initiate."
        ),
        "priority": TicketPriority.HIGH,
        "category": "Security",
        "subcategory": "MFA",
    },
]


def seed_customers(
    db: Session,
) -> dict[str, object]:
    customers = {}
    created = 0

    for customer_data in CUSTOMERS:
        email = customer_data["email"]

        customer = get_customer_by_email(
            db,
            email,
        )

        if customer is None:
            customer = create_customer(
                db,
                CustomerCreate(**customer_data),
            )
            created += 1

        customers[email] = customer

    print(f"Customers created: {created}")

    return customers


def seed_devices(
    db: Session,
    customers: dict[str, object],
) -> dict[str, object]:
    devices = {}
    created = 0

    for device_data in DEVICES:
        hostname = device_data["hostname"]

        existing = get_device_by_hostname(
            db,
            hostname,
        )

        if existing is None:
            existing = get_device_by_asset_tag(
                db,
                device_data["asset_tag"],
            )

        if existing is not None:
            devices[hostname] = existing
            continue

        customer_email = device_data["customer_email"]

        customer_id = None

        if customer_email is not None:
            customer_id = customers[customer_email].id

        device = create_device(
            db,
            DeviceCreate(
                asset_tag=device_data["asset_tag"],
                hostname=hostname,
                customer_id=customer_id,
                device_type=device_data["device_type"],
                status=device_data["status"],
                manufacturer=device_data["manufacturer"],
                model=device_data["model"],
                operating_system=device_data["operating_system"],
                os_version=device_data["os_version"],
                ip_address=device_data["ip_address"],
            ),
        )

        devices[hostname] = device
        created += 1

    print(f"Devices created: {created}")

    return devices


def seed_tickets(
    db: Session,
    customers: dict[str, object],
    devices: dict[str, object],
) -> None:
    created = 0

    for ticket_data in TICKETS:
        customer = customers[ticket_data["customer_email"]]

        existing_statement = select(Ticket).where(
            Ticket.customer_id == customer.id,
            Ticket.title == ticket_data["title"],
        )

        existing = db.scalar(existing_statement)

        if existing is not None:
            continue

        device_id = None

        hostname = ticket_data["device_hostname"]

        if hostname is not None:
            device_id = devices[hostname].id

        create_ticket(
            db,
            TicketCreate(
                title=ticket_data["title"],
                description=ticket_data["description"],
                priority=ticket_data["priority"],
                category=ticket_data["category"],
                subcategory=ticket_data["subcategory"],
                customer_id=customer.id,
                device_id=device_id,
            ),
        )

        created += 1

    print(f"Tickets created: {created}")


def seed_database() -> None:
    print("Starting development database seed...")

    with SessionLocal() as db:
        customers = seed_customers(db)

        devices = seed_devices(
            db,
            customers,
        )

        seed_tickets(
            db,
            customers,
            devices,
        )

    print("Development database seed complete.")


if __name__ == "__main__":
    seed_database()
