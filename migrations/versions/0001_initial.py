"""initial

Revision ID: 0001
Revises:
Create Date: 2023-08-12 01:48:40.873630
"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

from shared.database.models import Role
from shared.utils.enums import Roles

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "class_lessons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("grade", sa.String(length=2), nullable=False),
        sa.Column("letter", sa.String(length=1), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_class_lessons")),
        sa.UniqueConstraint("id", name=op.f("uq_class_lessons_id")),
    )
    op.create_table(
        "full_lessons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("grade", sa.String(length=2), nullable=False),
        sa.Column("image", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_full_lessons")),
        sa.UniqueConstraint("id", name=op.f("uq_full_lessons_id")),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_roles")),
        sa.UniqueConstraint("id", name=op.f("uq_roles_id")),
        sa.UniqueConstraint("role", name=op.f("uq_roles_role")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("createad_time", sa.DateTime(), nullable=False),
        sa.Column("modified_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("id", name=op.f("uq_users_id")),
    )
    op.create_index(op.f("ix_users_user_id"), "users", ["user_id"], unique=True)
    op.create_table(
        "laundries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("rings", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            name=op.f("fk_laundries_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_laundries")),
        sa.UniqueConstraint("id", name=op.f("uq_laundries_id")),
        sa.UniqueConstraint("user_id", name=op.f("uq_laundries_user_id")),
    )
    op.create_table(
        "menus",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("edit_by", sa.BigInteger(), nullable=True),
        sa.Column("breakfast", sa.String(), nullable=True),
        sa.Column("lunch", sa.String(), nullable=True),
        sa.Column("dinner", sa.String(), nullable=True),
        sa.Column("snack", sa.String(), nullable=True),
        sa.Column("supper", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["edit_by"],
            ["users.user_id"],
            name=op.f("fk_menus_edit_by_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_menus")),
        sa.UniqueConstraint("id", name=op.f("uq_menus_id")),
    )
    op.create_index(op.f("ix_menus_date"), "menus", ["date"], unique=True)
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("grade", sa.String(length=2), nullable=True),
        sa.Column("letter", sa.String(length=1), nullable=True),
        sa.Column("lessons_notify", sa.Boolean(), nullable=False),
        sa.Column("news_notify", sa.Boolean(), nullable=False),
        sa.Column("washing_time", sa.Integer(), nullable=False),
        sa.Column("drying_time", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            name=op.f("fk_settings_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_settings")),
        sa.UniqueConstraint("id", name=op.f("uq_settings_id")),
        sa.UniqueConstraint("user_id", name=op.f("uq_settings_user_id")),
    )
    op.create_table(
        "users_to_roles",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk_users_to_roles_role_id_roles"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            name=op.f("fk_users_to_roles_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("user_id", "role_id", name=op.f("pk_users_to_roles")),
    )

    conn = op.get_bind()
    for role in Roles.all_roles():
        conn.execute(sa.insert(Role).values(role=role))

    op.create_unique_constraint(op.f("uq_class_lessons_id"), "class_lessons", ["id"])
    op.create_unique_constraint(op.f("uq_full_lessons_id"), "full_lessons", ["id"])
    op.create_unique_constraint(op.f("uq_laundries_id"), "laundries", ["id"])
    op.create_unique_constraint(op.f("uq_menus_id"), "menus", ["id"])
    op.create_unique_constraint(op.f("uq_roles_id"), "roles", ["id"])
    op.create_unique_constraint(op.f("uq_settings_id"), "settings", ["id"])
    op.create_unique_constraint(op.f("uq_users_id"), "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_users_id"), "users", type_="unique")
    op.drop_constraint(op.f("uq_settings_id"), "settings", type_="unique")
    op.drop_constraint(op.f("uq_roles_id"), "roles", type_="unique")
    op.drop_constraint(op.f("uq_menus_id"), "menus", type_="unique")
    op.drop_constraint(op.f("uq_laundries_id"), "laundries", type_="unique")
    op.drop_constraint(op.f("uq_full_lessons_id"), "full_lessons", type_="unique")
    op.drop_constraint(op.f("uq_class_lessons_id"), "class_lessons", type_="unique")

    op.drop_table("users_to_roles")
    op.drop_table("settings")
    op.drop_index(op.f("ix_menus_date"), table_name="menus")
    op.drop_table("menus")
    op.drop_table("laundries")
    op.drop_index(op.f("ix_users_user_id"), table_name="users")
    op.drop_table("users")
    op.drop_table("roles")
    op.drop_table("full_lessons")
    op.drop_table("class_lessons")
    # ### end Alembic commands ###
