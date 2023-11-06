"""educators_schedules

Revision ID: 0002
Revises: 0001
Create Date: 2023-08-15 01:54:39.912725
"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "educators_schedules",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("edit_by", sa.BigInteger(), nullable=True),
        sa.Column("schedule", sa.String(length=1024), nullable=True),
        sa.ForeignKeyConstraint(
            ["edit_by"],
            ["users.user_id"],
            name=op.f("fk_educators_schedules_edit_by_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_educators_schedules")),
        sa.UniqueConstraint("id", name=op.f("uq_educators_schedules_id")),
    )
    op.create_index(
        op.f("ix_educators_schedules_date"),
        "educators_schedules",
        ["date"],
        unique=True,
    )
    op.create_unique_constraint(
        op.f("uq_educators_schedules_id"), "educators_schedules", ["id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_educators_schedules_date"), table_name="educators_schedules")
    op.drop_constraint(
        op.f("uq_educators_schedules_id"), "educators_schedules", type_="unique"
    )
    op.drop_table("educators_schedules")
    # ### end Alembic commands ###
