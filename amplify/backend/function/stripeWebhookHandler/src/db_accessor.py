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

def update_message_count_by_product_id(customer_id, line_user_id, product_id, next_update_date):
    if product_id == const.PRODUCT_ID_BASIC:
        message_count = 100
        plan = "basic"
    elif product_id == const.PRODUCT_ID_STANDARD:
        message_count = 300
        plan = "standard"
    elif product_id == const.PRODUCT_ID_PREMIUM:
        message_count = -1  # 無制限
        plan = "premium"
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
                            'UpdateExpression': 'SET message_count = :message_count, #plan = :plan, next_update_date = :next_update_date',
                            'ExpressionAttributeValues': {
                                ':message_count': {'N': str(message_count)},
                                ':plan': {'S': plan},
                                ':next_update_date': {'S': next_update_date}
                            },
                            'ExpressionAttributeNames': {
                                '#plan': 'plan'
                            }
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
                    UpdateExpression='SET #plan = :plan',
                    ExpressionAttributeValues={':plan': {'S': 'free'}},
                    ExpressionAttributeNames={'#plan': 'plan'}
                )

    except Exception as e:
        print(f"Error updating plan to free by customer ID: {e}")
        raise

def get_user_language_by_line_user_id(line_user_id: str) -> str:
    try:
        # line_user_idを使ってレコードを検索
        response = dynamodb.query(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            KeyConditionExpression='id = :line_user_id',
            ExpressionAttributeValues={':line_user_id': {'S': line_user_id}}
        )

        items = response['Items']

        if items:
            user_language = items[0]['user_language']['S']
            return user_language
        else:
            print("No matching record found for line_user_id.")
            return None

    except Exception as e:
        print(f"Error getting user_language by line_user_id: {e}")
        raise

def get_flag_payment_by_line_user_id(line_user_id: str) -> int:
    try:
        # line_user_idを使ってレコードを検索
        response = dynamodb.query(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            KeyConditionExpression='id = :line_user_id',
            ExpressionAttributeValues={':line_user_id': {'S': line_user_id}}
        )

        items = response['Items']

        if items:
            flag_payment = int(items[0]['flag_payment']['N'])
            return flag_payment
        else:
            print("No matching record found for line_user_id.")
            return None

    except Exception as e:
        print(f"Error getting flag_payment by line_user_id: {e}")
        raise


def set_flag_payment_to_one_by_line_user_id(line_user_id: str) -> None:
    try:
        # line_user_idを使ってレコードを検索
        response = dynamodb.query(
            TableName=MESSAGE_COUNT_TABLE_NAME,
            KeyConditionExpression='id = :line_user_id',
            ExpressionAttributeValues={':line_user_id': {'S': line_user_id}}
        )

        items = response['Items']

        if items:
            # ヒットしたレコードに対して、flag_paymentを1に更新
            dynamodb.update_item(
                TableName=MESSAGE_COUNT_TABLE_NAME,
                Key={'id': {'S': items[0]['id']['S']}},
                UpdateExpression='SET flag_payment = :flag_payment',
                ExpressionAttributeValues={':flag_payment': {'N': str(1)}}
            )
        else:
            print("No matching record found for line_user_id.")

    except Exception as e:
        print(f"Error setting flag_payment to one by line_user_id: {e}")
        raise