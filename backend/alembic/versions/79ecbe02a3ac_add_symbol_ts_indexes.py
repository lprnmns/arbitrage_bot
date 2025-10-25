"""Add indexes on symbol + ts_ns"""

from alembic import op


revision = "79ecbe02a3ac"
down_revision = "8d3e41d1c1cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("idx_ticks_symbol_ts_ns", "ticks", ["symbol", "ts_ns"], unique=False)
    op.create_index("idx_trades_symbol_ts_ns", "trades", ["symbol", "ts_ns"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_trades_symbol_ts_ns", table_name="trades")
    op.drop_index("idx_ticks_symbol_ts_ns", table_name="ticks")
