"""alter doors table

Revision ID: 4d8c106d096f
Revises: fdf8821871d7
Create Date: 2021-01-11 21:39:37.081723

"""
from alembic import op
import sqlalchemy as sa


revision = '4d8c106d096f'
down_revision = 'fdf8821871d7'
branch_labels = None
depends_on = None

def upgrade_doors_table() -> None:
    with op.batch_alter_table("doors") as batch_op:
        batch_op.add_column(sa.Column('access_token', sa.Text))
        batch_op.add_column(sa.Column('refresh_token', sa.Text))
        batch_op.add_column(sa.Column('access_token_expires', sa.DateTime))

def upgrade() -> None:
    upgrade_doors_table()

def downgrade() -> None:
    with op.batch_alter_table("doors") as batch_op:
        batch_op.drop_column('access_token')
        batch_op.drop_column('refresh_token')
        batch_op.drop_column('access_token_expires')
