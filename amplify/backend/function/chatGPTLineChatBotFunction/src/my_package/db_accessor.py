import boto3
from datetime import datetime
from . import const

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
        'IndexName': QUERY_INDEX_NAME,
        'KeyConditionExpression': '#lineUserId = :lineUserId',
        'ExpressionAttributeNames': {
            '#lineUserId': 'lineUserId'
        },
        'ExpressionAttributeValues': {
            ':lineUserId': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.query(**query_params)
        print("check_line_user_id_exists_query_result:",query_result)
        if query_result['Items']:
            return "Yes"
        else:
            return "No"
    except Exception as e:
        raise e

def decrement_message_count(line_user_id: str) -> None:
    message_count = get_message_count(line_user_id)
    if message_count is not None:
        update_params = {
            'TableName': MESSAGE_COUNT_TABLE_NAME,
            'Key': {
                'lineUserId': {'S': line_user_id}
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
        'IndexName': 'byLineUserId',
        'KeyConditionExpression': '#lineUserId = :lineUserId',
        'ExpressionAttributeNames': {
            '#lineUserId': 'lineUserId'
        },
        'ExpressionAttributeValues': {
            ':lineUserId': {'S': line_user_id}
        },
    }

    try:
        query_result = dynamodb.query(**query_params)
        if query_result['Items']:
            message_count_item = query_result['Items'][0]
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
            'id': {'S': str(uuid.uuid4())},
            'lineUserId': {'S': line_user_id},
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

