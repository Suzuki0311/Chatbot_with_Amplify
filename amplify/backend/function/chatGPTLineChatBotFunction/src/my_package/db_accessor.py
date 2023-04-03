import os
import boto3
from datetime import datetime
from . import const

TABLE_NAME = f'Messages{const.DB_TABLE_NAME_POSTFIX}'
QUERY_INDEX_NAME = 'byLineUserId'

# 環境変数 IS_LOCAL をチェック
is_local = os.environ.get('IS_LOCAL', 'False') == 'True'

if is_local:
    # ローカル環境の場合、DynamoDBクライアントを作成し、エンドポイントを指定
    dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:62224')
    TABLE_NAME = 'MessagesLocal'
else:
    # 本番環境の場合、DynamoDBクライアントを作成し、エンドポイントはデフォルトにする
    dynamodb = boto3.client('dynamodb')


def query_by_line_user_id(line_user_id: str, limit: int) -> list:
    # Create a dictionary of query parameters
    query_params = {
        'TableName': TABLE_NAME,
        'IndexName': QUERY_INDEX_NAME,
        # Use a named parameter for the key condition expression
        'KeyConditionExpression': '#lineUserId = :lineUserId',
        # Define an expression attribute name for the hash key
        'ExpressionAttributeNames': {
            '#lineUserId': 'lineUserId'
        },
        # Define an expression attribute value for the hash key
        'ExpressionAttributeValues': {
            ':lineUserId': {'S': line_user_id}
        },
        # Sort the results in descending order by sort key
        'ScanIndexForward': False,
        # Limit the number of results
        'Limit': limit
    }
    print("query_params:",query_params)

    try:
        # Call the query method of the DynamoDB client with the query parameters
        query_result = dynamodb.query(**query_params)
        print("query_params:",query_params)
        # Return the list of items from the query result
        return query_result['Items']
    except Exception as e:
        # Raise any exception that occurs during the query operation
        raise e


def put_message(partition_key: str, uid: str, role: str, content: str, now: datetime) -> None:
    # Create a dictionary of options for put_item
    options = {
        'TableName': TABLE_NAME,
        'Item': {
            'id': {'S': partition_key},
            'lineUserId': {'S': uid},
            'role': {'S': role},
            'content': {'S': content},
            'createdAt': {'S': now.isoformat()},
        },
    }
    print("options:",options)
    # Try to put the item into the table using dynamodb client
    try:
        dynamodb.put_item(**options)

    # If an exception occurs, re-raise it
    except Exception as e:
        raise e