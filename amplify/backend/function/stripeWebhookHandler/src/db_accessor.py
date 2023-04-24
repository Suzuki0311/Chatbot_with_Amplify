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