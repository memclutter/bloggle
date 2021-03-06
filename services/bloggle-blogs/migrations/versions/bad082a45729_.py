"""empty message

Revision ID: bad082a45729
Revises: 
Create Date: 2018-01-13 21:59:17.077460

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bad082a45729'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog',
    sa.Column('guid', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('user_guid', postgresql.UUID(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('about', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_blog_guid'), 'blog', ['guid'], unique=True)
    op.create_index(op.f('ix_blog_title'), 'blog', ['title'], unique=False)
    op.create_index(op.f('ix_blog_user_guid'), 'blog', ['user_guid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_user_guid'), table_name='blog')
    op.drop_index(op.f('ix_blog_title'), table_name='blog')
    op.drop_index(op.f('ix_blog_guid'), table_name='blog')
    op.drop_table('blog')
    # ### end Alembic commands ###
