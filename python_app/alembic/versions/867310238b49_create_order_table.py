"""create order table

Revision ID: 867310238b49
Revises: aef9cfabaf7d
Create Date: 2022-07-19 23:14:47.823981

"""
from alembic import op
import sqlalchemy as sa
from email.policy import default


# revision identifiers, used by Alembic.
revision = '867310238b49'
down_revision = ''
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'order',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('status', sa.String(50)),
    )


def downgrade():
    op.drop_table('order')
