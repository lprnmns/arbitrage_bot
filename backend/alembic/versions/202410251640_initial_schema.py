"""Initial ticks and trades tables"""
from alembic import op
import sqlalchemy as sa

revision = "202410251640"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ticks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("best_bid", sa.Float(), nullable=False),
        sa.Column("best_ask", sa.Float(), nullable=False),
        sa.Column("spread_bps", sa.Float(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="HL"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_ticks_symbol", "ticks", ["symbol"])

    op.create_table(
        "trades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("side", sa.String(length=4), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("size", sa.Float(), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="HL"),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_trades_symbol", "trades", ["symbol"])


def downgrade() -> None:
    op.drop_index("ix_trades_symbol", table_name="trades")
    op.drop_table("trades")
    op.drop_index("ix_ticks_symbol", table_name="ticks")
    op.drop_table("ticks")
