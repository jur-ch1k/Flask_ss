"""empty message

Revision ID: 524184b6d372
Revises: 813c6b8fde50
Create Date: 2023-04-04 10:59:13.010854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '524184b6d372'
down_revision = '813c6b8fde50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('var_folder', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('var_num', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'var_num')
    op.drop_column('user', 'var_folder')
    # ### end Alembic commands ###
