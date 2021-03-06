"""added uploadedfile

Revision ID: 3c6af282478
Revises: 13e98833cea
Create Date: 2015-04-02 13:25:34.978912

"""

# revision identifiers, used by Alembic.
revision = '3c6af282478'
down_revision = '13e98833cea'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('uploaded_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=1024), nullable=True),
    sa.Column('path', sa.String(length=1024), nullable=True),
    sa.Column('md5', sa.String(length=32), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_blog_post_slug', table_name='blog_post')
    op.create_index(op.f('ix_blog_post_slug'), 'blog_post', ['slug'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_post_slug'), table_name='blog_post')
    op.create_index('ix_blog_post_slug', 'blog_post', ['slug'], unique=False)
    op.drop_table('uploaded_file')
    ### end Alembic commands ###
