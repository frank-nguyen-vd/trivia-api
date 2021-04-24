"""empty message

Revision ID: f3ae826cff7e
Revises: 
Create Date: 2021-04-24 11:21:14.502028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3ae826cff7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('category', 'questions', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('category', 'questions', 'categories', ['category'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    # ### end Alembic commands ###