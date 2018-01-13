"""empty message

Revision ID: 3250fc9d3940
Revises: 990ba0210128
Create Date: 2018-01-13 22:51:18.792876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3250fc9d3940'
down_revision = '990ba0210128'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TRIGGER "comment_timestamps"
            BEFORE INSERT OR UPDATE ON "comment"
            FOR EACH ROW EXECUTE PROCEDURE table_timestamps();
    """)


def downgrade():
    op.execute("""
        DROP TRIGGER IF EXISTS "comment_timestamps" ON "comment";
    """)
