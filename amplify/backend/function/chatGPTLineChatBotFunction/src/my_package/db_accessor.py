import boto3
from datetime import datetime
from . import const
import uuid
from datetime import datetime, timedelta



TABLE_NAME = f'Messages{const.DB_TABLE_NAME_POSTFIX}'
MESSAGE_COUNT_TABLE_NAME = f'MessageCount{const.DB_TABLE_NAME_POSTFIX}'
QUERY_INDEX_NAME = 'byLineUserId'

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

def check_line_user_id_exists(line_user_id: str) -> str:
    query_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.get_item(**query_params)
        print("check_line_user_id_exists_query_result:", query_result)
        if 'Item' in query_result:
            return "Yes"
        else:
            return "No"
    except Exception as e:
        raise e

def decrement_message_count(line_user_id: str, message_count: int) -> None:
    update_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': line_user_id}
        },
        'UpdateExpression': 'SET message_count = :new_count',
        'ExpressionAttributeValues': {
            ':new_count': {'N': str(message_count - 1)}
        }
    }

    try:
        dynamodb.update_item(**update_params)
    except Exception as e:
        raise e

def get_current_message_count(line_user_id: str) -> int:
    query_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.get_item(**query_params)
        if 'Item' in query_result:
            message_count_item = query_result['Item']
            message_count = int(message_count_item['message_count']['N'])
            return message_count
        else:
            return None
    except Exception as e:
        raise e

def create_or_check_line_user_id(line_user_id: str) -> str:
    now = datetime.now().isoformat()
    put_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Item': {
            'id': {'S': line_user_id},
            'customerId': {'S': ''},
            'plan': {'S': 'free'},
            'first_purchase_date': {'S': now},
            'updated_purchase_date': {'S': now},
            'message_count': {'N': str(30)}
        }
    }

    try:
        dynamodb.put_item(**put_params)
        return f"New lineUserId {line_user_id} added to the table with a free plan and message_count of 30."
    except Exception as e:
        raise e


def get_line_user_data(line_user_id: str) -> dict:
    query_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.get_item(**query_params)
        if 'Item' in query_result:
            user_data = {
                'plan': query_result['Item']['plan']['S'],
                'message_count': int(query_result['Item']['message_count']['N'])
            }
            return user_data
        else:
            return None
    except Exception as e:
        raise e

def insert_data(line_user_id: str, user_language: str) -> None:
    now = datetime.now()
    now_iso = now.isoformat()
    next_update_date = now + timedelta(days=30)
    next_update_date_iso = next_update_date.isoformat()

    put_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Item': {
            'id': {'S': line_user_id},
            'plan': {'S': 'free'},
            'first_purchase_date': {'S': now_iso},
            'updated_purchase_date': {'S': now_iso},
            'next_update_date': {'S': next_update_date_iso},  # 追加
            'message_count': {'N': str(7)},
            'user_language': {'S': user_language}
        }
    }

    try:
        dynamodb.put_item(**put_params)
    except Exception as e:
        raise e

def get_user_plan(line_user_id: str) -> str:
    query_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.get_item(**query_params)
        if 'Item' in query_result:
            user_plan = query_result['Item']['plan']['S']
            return user_plan
        else:
            return None
    except Exception as e:
        raise e

def get_customer_id_by_line_user_id(id: str) -> str:
    query_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': id}
        },
    }

    try:
        query_result = dynamodb.get_item(**query_params)
        if 'Item' in query_result:
            customer_id = query_result['Item']['customerId']['S']
            return customer_id
        else:
            return None
    except Exception as e:
        raise e

def get_next_update_date(line_user_id: str) -> str:
    query_params = {
        'TableName': MESSAGE_COUNT_TABLE_NAME,
        'Key': {
            'id': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.get_item(**query_params)
        if 'Item' in query_result:
            next_update_date_str = query_result['Item']['next_update_date']['S']
            next_update_date = datetime.strptime(next_update_date_str, '%Y-%m-%dT%H:%M:%S%z')
            next_update_date_plus_one = next_update_date + timedelta(days=1)
            formatted_next_update_date = next_update_date_plus_one.strftime('%Y-%m-%d')
            return formatted_next_update_date
        else:
            return None
    except Exception as e:
        raise e