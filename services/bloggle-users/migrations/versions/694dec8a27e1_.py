"""empty message

Revision ID: 694dec8a27e1
Revises: c017234dd4b1
Create Date: 2018-01-13 21:15:23.024697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '694dec8a27e1'
down_revision = 'c017234dd4b1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TRIGGER "user_timestamps"
            BEFORE INSERT OR UPDATE ON "user"
            FOR EACH ROW EXECUTE PROCEDURE table_timestamps();
    """)


def downgrade():
    op.execute("""
        DROP TRIGGER IF EXISTS "user_timestamps" ON "user";
    """)
