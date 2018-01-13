"""empty message

Revision ID: 7c83246438d0
Revises: 701d82dcd063
Create Date: 2018-01-13 22:00:57.257468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c83246438d0'
down_revision = '701d82dcd063'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TRIGGER "blog_timestamps"
            BEFORE INSERT OR UPDATE ON "blog"
            FOR EACH ROW EXECUTE PROCEDURE table_timestamps();
    """)


def downgrade():
    op.execute("""
        DROP TRIGGER IF EXISTS "blog_timestamps" ON "blog";
    """)
