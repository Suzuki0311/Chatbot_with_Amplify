import os
# from . import aws_systems_manager
import aws_systems_manager

BASE_SECRET_PATH = os.environ.get('BASE_SECRET_PATH')
BASE_SECRET_CHATGPTLINECHATBOTFUNCTION_PATH = os.environ.get('BASE_SECRET_CHATGPTLINECHATBOTFUNCTION_PATH')
DB_TABLE_NAME_POSTFIX = os.environ.get('DB_TABLE_NAME_POSTFIX')
PRODUCT_ID_BASIC = os.environ.get('PRODUCT_ID_BASIC') 
PRODUCT_ID_STANDARD = os.environ.get('PRODUCT_ID_STANDARD') 
PRODUCT_ID_PREMIUM = os.environ.get('PRODUCT_ID_PREMIUM') 
STRIPE_API_KEY = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}STRIPE_API_KEY')
LINE_CHANNEL_ACCESS_TOKEN = aws_systems_manager.get_secret(f'{BASE_SECRET_CHATGPTLINECHATBOTFUNCTION_PATH}LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = aws_systems_manager.get_secret(f'{BASE_SECRET_CHATGPTLINECHATBOTFUNCTION_PATH}LINE_CHANNEL_SECRET')
endpoint_secret = aws_systems_manager.get_secret(f'{BASE_SECRET_PATH}endpoint_secret')