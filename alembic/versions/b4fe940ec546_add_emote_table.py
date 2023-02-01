"""add emote table

Revision ID: b4fe940ec546
Revises: 
Create Date: 2023-02-01 13:10:40.467369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4fe940ec546'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'emotes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(15), nullable=False),
        sa.Column('owner', sa.String(25), nullable=False),
        sa.Column('access', sa.Boolean, nullable=False),
        sa.Column('image', sa.LargeBinary, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('emotes')

