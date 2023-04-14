import os
# import aws_systems_manager
from . import aws_systems_manager


is_local = os.environ.get('IS_LOCAL', 'False') == 'True'

if is_local:
    OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
else:
    BASE_SECRET_PATH = os.environ.get('BASE_SECRET_PATH')
    DB_TABLE_NAME_POSTFIX = os.environ.get('DB_TABLE_NAME_POSTFIX')
    OPEN_AI_API_KEY = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}OPEN_AI_API_KEY')
    LINE_CHANNEL_SECRET = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}LINE_CHANNEL_SECRET')
    LINE_CHANNEL_ACCESS_TOKEN = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}LINE_CHANNEL_ACCESS_TOKEN')
    GOOGLE_APPLICATION_CREDENTIALS = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}GOOGLE_APPLICATION_CREDENTIALS')
    DB_HOST = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}DB_HOST')
    DB_USER = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}DB_USER')
    DB_PASSWORD = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}DB_PASSWORD')
    DB_NAME = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}DB_NAME')