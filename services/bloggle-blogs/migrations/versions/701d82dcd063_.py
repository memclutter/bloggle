"""empty message

Revision ID: 701d82dcd063
Revises: bad082a45729
Create Date: 2018-01-13 22:00:10.222058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '701d82dcd063'
down_revision = 'bad082a45729'
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
