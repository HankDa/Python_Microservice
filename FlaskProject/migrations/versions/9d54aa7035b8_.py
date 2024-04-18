"""empty message

Revision ID: 9d54aa7035b8
Revises: 2c3a00d1fdbc
Create Date: 2024-04-18 21:00:46.420304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d54aa7035b8'
down_revision = '2c3a00d1fdbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products_user2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products_user2')
    # ### end Alembic commands ###
