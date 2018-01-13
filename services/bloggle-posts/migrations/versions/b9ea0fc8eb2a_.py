"""empty message

Revision ID: b9ea0fc8eb2a
Revises: 8b789d67fe62
Create Date: 2018-01-13 22:26:41.991827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9ea0fc8eb2a'
down_revision = '8b789d67fe62'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION "table_timestamps"() RETURNS TRIGGER AS $table_timestamps$
          BEGIN
            IF (TG_OP = 'INSERT') THEN
              NEW.created_at = now();
              RETURN NEW;
            ELSIF (TG_OP = 'UPDATE') THEN
              NEW.created_at = OLD.created_at;
              NEW.updated_at = now();
              RETURN NEW;
            END IF;
          END;
        $table_timestamps$ LANGUAGE plpgsql;
    """)


def downgrade():
    op.execute("""
        DROP FUNCTION IF EXISTS table_timestamps();
    """)
