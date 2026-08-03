"""rename batch mentor column to mentor_id

Revision ID: f3a2c7e19d5b
Revises: 660133dd1861
Create Date: 2026-08-03 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a2c7e19d5b'
down_revision = '660133dd1861'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('batches', 'mentor', new_column_name='mentor_id')


def downgrade() -> None:
    op.alter_column('batches', 'mentor_id', new_column_name='mentor')
