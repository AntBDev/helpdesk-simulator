"""add ticket number sequence

Revision ID: b92d2f7b66b1
Revises: c8ef39eea698
Create Date: 2026-09-14 15:17:24.674081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b92d2f7b66b1'
down_revision: Union[str, Sequence[str], None] = 'c8ef39eea698'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE SEQUENCE ticket_number_seq "
        "START WITH 1 INCREMENT BY 1"
    )


def downgrade() -> None:
    op.execute(
        "DROP SEQUENCE IF EXISTS ticket_number_seq"
    )
