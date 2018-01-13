"""empty message

Revision ID: c017234dd4b1
Revises: 732a5f52477c
Create Date: 2018-01-13 21:14:38.413253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c017234dd4b1'
down_revision = '732a5f52477c'
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
