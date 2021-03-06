"""empty message

Revision ID: 2d7346a90e72
Revises: 95e499c2fcd1
Create Date: 2020-01-23 15:36:05.851213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2d7346a90e72'
down_revision = '95e499c2fcd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('post', sa.Column('post', sa.String(length=1000), nullable=False))
    op.add_column('post', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_column('post', 'title')
    op.drop_column('post', 'content')
    op.drop_column('post', 'image')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image', mysql.VARCHAR(length=255), nullable=False))
    op.add_column('post', sa.Column('content', mysql.VARCHAR(length=255), nullable=False))
    op.add_column('post', sa.Column('title', mysql.VARCHAR(length=255), nullable=False))
    op.drop_column('post', 'user_id')
    op.drop_column('post', 'updated_at')
    op.drop_column('post', 'post')
    op.drop_column('post', 'created_at')
    # ### end Alembic commands ###
