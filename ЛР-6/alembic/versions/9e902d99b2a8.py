from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9e902d99b2a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("user",
            Column("iduser", Integer, primary_key = True),
            Column("username", String(45), nullable = False),
            Column("full_name", String(45), nullable = False),
            Column("phone_number", String(45), nullable = False),
            Column("email", String(45), nullable = False)
    )
    op.create_table("order",
            Column("idorder", Integer, primary_key = True),
            Column("delivery_adress", String(45), nullable = False),
            Column("status", Enum("confirmation", "shipping", "completed"), nullable = False),
            Column("user_id", Integer, ForeignKey("user.iduser"))

    )
    op.create_table("trainer",
            Column("idtrainer", Integer, primary_key = True),
            Column("name", String(45), nullable = False),
            Column("size", Float, nullable = False),
            Column("price", Float, nullable = False)
    )
    op.create_table("order_and_trainer",
            Column("order_id", Integer, ForeignKey("order.idorder")),
            Column("trainer_id", Integer, ForeignKey("trainer.idtrainer")),
            Column("count", Integer, primary_key = True),
    )


def downgrade() -> None:
    op.drop_table("order_and_trainer")
    op.drop_table("order")
    op.drop_table("trainer")
    op.drop_table("user")
