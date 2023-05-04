import os
# import aws_systems_manager
from . import aws_systems_manager

BASE_SECRET_PATH = os.environ.get('BASE_SECRET_PATH')
BASE_SECRET_PATH_STRIPE = os.environ.get('BASE_SECRET_PATH_STRIPE')
DB_TABLE_NAME_POSTFIX = os.environ.get('DB_TABLE_NAME_POSTFIX')
PRODUCT_URL_BASIC = os.environ.get('PRODUCT_URL_BASIC') 
PRODUCT_URL_STANDARD = os.environ.get('PRODUCT_URL_STANDARD') 
PRODUCT_URL_PREMIUM = os.environ.get('PRODUCT_URL_PREMIUM') 
PRICE_ID_BASIC = os.environ.get('PRICE_ID_BASIC')
PRICE_ID_STANDARD = os.environ.get('PRICE_ID_STANDARD') 
PRICE_ID_PREMIUM = os.environ.get('PRICE_ID_PREMIUM') 
OPEN_AI_API_KEY = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}OPEN_AI_API_KEY')
LINE_CHANNEL_SECRET = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}LINE_CHANNEL_ACCESS_TOKEN')
GOOGLE_APPLICATION_CREDENTIALS = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}GOOGLE_APPLICATION_CREDENTIALS')
STRIPE_API_KEY = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH_STRIPE}STRIPE_API_KEY')