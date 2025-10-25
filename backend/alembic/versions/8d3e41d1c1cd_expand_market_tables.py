"""Expand market tables with HL ingestion columns."""
from alembic import op
import sqlalchemy as sa

revision = "8d3e41d1c1cd"
down_revision = "202410251640"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("ticks") as batch:
        batch.add_column(sa.Column("ts_ns", sa.BigInteger(), nullable=False, server_default="0"))
        batch.add_column(sa.Column("venue", sa.String(length=32), nullable=False, server_default="HL"))
        batch.add_column(sa.Column("best_bid_size", sa.Float(), nullable=False, server_default="0"))
        batch.add_column(sa.Column("best_ask_size", sa.Float(), nullable=False, server_default="0"))
    op.create_index("ix_ticks_ts_ns", "ticks", ["ts_ns"], unique=False)

    with op.batch_alter_table("trades") as batch:
        batch.add_column(sa.Column("venue", sa.String(length=32), nullable=False, server_default="HL"))
        batch.add_column(sa.Column("ts_ns", sa.BigInteger(), nullable=False, server_default="0"))
    op.create_index("ix_trades_ts_ns", "trades", ["ts_ns"], unique=False)

    with op.batch_alter_table("ticks") as batch:
        batch.alter_column("ts_ns", server_default=None)
        batch.alter_column("best_bid_size", server_default=None)
        batch.alter_column("best_ask_size", server_default=None)
    with op.batch_alter_table("trades") as batch:
        batch.alter_column("ts_ns", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("trades") as batch:
        batch.drop_column("ts_ns")
        batch.drop_column("venue")
    op.drop_index("ix_trades_ts_ns", table_name="trades")

    with op.batch_alter_table("ticks") as batch:
        batch.drop_column("best_ask_size")
        batch.drop_column("best_bid_size")
        batch.drop_column("venue")
        batch.drop_column("ts_ns")
    op.drop_index("ix_ticks_ts_ns", table_name="ticks")
