"""empty message

Revision ID: 85f213730a3d
Revises: b9ea0fc8eb2a
Create Date: 2018-01-13 22:27:27.086460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85f213730a3d'
down_revision = 'b9ea0fc8eb2a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TRIGGER "post_timestamps"
            BEFORE INSERT OR UPDATE ON "post"
            FOR EACH ROW EXECUTE PROCEDURE table_timestamps();
    """)


def downgrade():
    op.execute("""
        DROP TRIGGER IF EXISTS "post_timestamps" ON "post";
    """)
