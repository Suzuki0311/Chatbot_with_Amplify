import os
from . import aws_systems_manager

BASE_SECRET_PATH = os.environ.get('BASE_SECRET_PATH')
DB_TABLE_NAME_POSTFIX = os.environ.get('DB_TABLE_NAME_POSTFIX')
STRIPE_API_KEY = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}STRIPE_API_KEY')
