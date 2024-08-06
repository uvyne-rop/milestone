"""Initial migration.

Revision ID: 7e43f44c06e7
Revises: c0655e96b642
Create Date: 2024-08-06 15:07:11.308846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e43f44c06e7'
down_revision = 'c0655e96b642'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('space', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('space', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
