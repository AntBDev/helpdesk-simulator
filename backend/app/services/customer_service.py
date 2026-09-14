from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def get_customers(db: Session) -> list[Customer]:
    statement = select(Customer).order_by(Customer.id)

    return list(db.scalars(statement).all())


def get_customer_by_id(
    db: Session,
    customer_id: int,
) -> Customer | None:
    return db.get(Customer, customer_id)


def get_customer_by_email(
    db: Session,
    email: str,
) -> Customer | None:
    statement = select(Customer).where(Customer.email == email)

    return db.scalar(statement)


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> Customer:
    customer = Customer(**customer_data.model_dump())

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer
