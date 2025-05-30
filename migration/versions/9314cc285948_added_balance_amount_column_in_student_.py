"""Added balance_amount column in student_batches table.

Revision ID: 9314cc285948
Revises: 49f574732fdb
Create Date: 2025-05-04 13:32:10.721226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9314cc285948'
down_revision = '49f574732fdb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_batches', sa.Column('balance_amount', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student_batches', 'balance_amount')
    # ### end Alembic commands ###
