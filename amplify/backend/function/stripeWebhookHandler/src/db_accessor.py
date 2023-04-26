import boto3
# from . import const
import const

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

    response = None
    if customer_id:
        response = dynamodb.query(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            IndexName='customerId-index',
            KeyConditionExpression='customerId = :customer_id',
            ExpressionAttributeValues={':customer_id': {'S': customer_id}}
        )

    if not response or not response['Items']:
        if line_user_id:
            response = dynamodb.query(
                TableName=MESSAGE_COUNT_TABLE_NAME,
                KeyConditionExpression='id = :line_user_id',
                ExpressionAttributeValues={':line_user_id': {'S': line_user_id}}
            )

    if not response or not response['Items']:
        raise ValueError("No matching record found for customer_id and line_user_id")

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

def get_line_user_id_by_customer_id(customer_id):
    response = dynamodb.query(
        TableName=MESSAGE_COUNT_TABLE_NAME,
        IndexName='customerId-index',
        KeyConditionExpression='customerId = :customer_id',
        ExpressionAttributeValues={':customer_id': {'S': customer_id}}
    )
    items = response['Items']

    if items:
        line_user_id = items[0]['id']['S']
        return line_user_id
    else:
        print("No matching record found for customer_id.")
        return None

def update_plan_to_free_by_customer_id(customer_id):
    try:
        # customerIdを使ってレコードを検索
        response = search_customer_in_table(customer_id)

        if not response:
            print(f"Customer ID {customer_id} not found.")
            return

        # ヒットしたレコードに対して、planをfreeに更新
        for item in response:
            dynamodb.update_item(
                TableName=MESSAGE_COUNT_TABLE_NAME,
                Key={'id': {'S': item['id']['S']}},
                UpdateExpression='SET plan = :plan',
                ExpressionAttributeValues={':plan': {'S': 'free'}}
            )
    except Exception as e:
        print(f"Error updating plan to free by customer ID: {e}")
        raise