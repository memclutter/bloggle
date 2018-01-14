import os

from common import create_app

app = create_app(os.getenv('APP_ENV'))
