import boto3
from . import const

MESSAGE_COUNT_TABLE_NAME = f'MessageCount{const.DB_TABLE_NAME_POSTFIX}'
dynamodb = boto3.client('dynamodb')

def search_customer_in_table(customer_id):
    response = dynamodb.query(
        TableName=MESSAGE_COUNT_TABLE_NAME,
        IndexName='customerId-index',
        KeyConditionExpression='customerId = :customer_id',
        ExpressionAttributeValues={':customer_id': {'S': customer_id}}
    )
    return response['Items']

def update_customer_id_by_client_reference_id(client_reference_id, customer_id):
    try:
        response = dynamodb.get_item(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            Key={'id': {'S': client_reference_id}}
        )

        if 'Item' not in response:
            print(f"Client reference ID {client_reference_id} not found.")
            return

        item = response['Item']
        dynamodb.update_item(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            Key={'id': {'S': item['id']['S']}},
            UpdateExpression='SET customerId = :customer_id',
            ExpressionAttributeValues={':customer_id': {'S': customer_id}}
        )
    except Exception as e:
        print(f"Error updating customer ID by client reference ID: {e}")
        raise

def update_message_count_by_product_id(customer_id, line_user_id, product_id):
    if product_id == const.PRODUCT_ID_BASIC:
        message_count = 100
    elif product_id == const.PRODUCT_ID_STANDARD:
        message_count = 300
    elif product_id == const.PRODUCT_ID_PREMIUM:
        message_count = -1  # 無制限
    else:
        raise ValueError("Invalid product_id")

    if customer_id:
        response = dynamodb.query(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            IndexName='customerId-index',
            KeyConditionExpression='customerId = :customer_id',
            ExpressionAttributeValues={':customer_id': {'S': customer_id}}
        )
    else:
        response = dynamodb.query(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            KeyConditionExpression='id = :line_user_id',
            ExpressionAttributeValues={':line_user_id': {'S': line_user_id}}
        )

    items = response['Items']
    if items:
        item = items[0]
        update_params = {
            'TableName': MESSAGE_COUNT_TABLE_NAME,
            'Key': {'id': item['id']},
            'UpdateExpression': 'SET message_count = :message_count',
            'ExpressionAttributeValues': {':message_count': {'N': str(message_count)}}
        }
        dynamodb.update_item(**update_params)
    else:
        print("No matching record found.")