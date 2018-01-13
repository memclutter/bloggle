import os

from flask_migrate import Migrate

from common import create_app, db

app = create_app(os.getenv('APP_ENV'))
migrate = Migrate(app, db)
