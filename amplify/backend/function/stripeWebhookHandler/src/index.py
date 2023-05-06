print("index.pyは起動している")
import json
import const
import db_accessor
import stripe
from botocore.exceptions import ClientError
import time
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

stripe.api_key = const.STRIPE_API_KEY

# LINE Botのアクセストークンとシークレットを設定
LINE_CHANNEL_ACCESS_TOKEN = const.LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET = const.LINE_CHANNEL_SECRET

# LINE Bot APIの初期化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def get_product_id(event_type, event_data):
    product_id = None

    if event_type == 'checkout.session.completed':
        session_id = event_data['data']['object']['id']
        line_items = stripe.checkout.Session.list_line_items(session_id)
        product_id = line_items['data'][0]['price']['product']

    elif event_type == 'customer.subscription.updated':
        product_id = event_data.get('data', {}).get('object', {}).get('items', {}).get('data', [])[0].get('price', {}).get('product')

    elif event_type == 'invoice.payment_succeeded':
        invoice_id = event_data['data']['object']['id']
        invoice = stripe.Invoice.retrieve(invoice_id)
        print("invoice:",invoice)
        for line_item in invoice["lines"]["data"]:
            if not line_item["proration"]:
                product_id = line_item["price"]["product"]
                break

    return product_id


def handler(event, context):
    print('received event:')
    print(event)
    
    # Parse the 'body' key
    body = json.loads(event['body'])

    # Get the 'type' key from the parsed body
    event_type = body.get('type', '')

    if event_type == 'checkout.session.completed': #初回購入時にline_user_idとcustomer_idをDBに紐づけて登録
        print("checkout.session.completedイベント発行")
        session = body['data']['object']

        line_user_id = session.get('client_reference_id')
        print("line_user_id_client_reference_id:", line_user_id)

        customer_id = session['customer']
        print("customer_id:", customer_id)

        product_id = get_product_id(event_type, body)
        print("product_id:", product_id)

        items = db_accessor.search_customer_in_table(customer_id)
        if not items:  # リストが空の場合
            print("顧客IDがテーブルに存在しません。")
            db_accessor.update_customer_id_by_client_reference_id(line_user_id, customer_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Successfully processed checkout.session.completed event'})
        }

        # try:
        #     db_accessor.update_message_count_by_product_id(customer_id, line_user_id, product_id)
        #     print("正常にユーザーの回数がアップデートされました")
        # except ValueError as e:
        #     print("Error updating message count:", e)

    # elif event_type == 'customer.subscription.updated': #サブスクリプション更新時
    #     customer_id = body.get('data', {}).get('object', {}).get('customer')
    #     print("customer.subscription.updatedイベントのcustomer_id:",customer_id)

    #     line_user_id = db_accessor.get_line_user_id_by_customer_id(customer_id)
    #     print("customer.subscription.updatedイベントのline_user_id:",line_user_id)

    #     product_id = get_product_id(event_type, body)
    #     print("customer.subscription.updatedイベントのproduct_id:",product_id)

    #     # 商品IDと顧客IDを使用して、メッセージの送信可能回数を更新
    #     try:
    #         db_accessor.update_message_count_by_product_id(customer_id, line_user_id, product_id)
        
    #     except ValueError as e:
    #         print("Error updating message count:", e)

    elif event_type == 'invoice.payment_succeeded': #支払い完了時
        print("invoice.payment_succeededイベント発行")
        def wait_for_line_user_id(customer_id, retries=5, delay=1):
            for _ in range(retries):
                line_user_id = db_accessor.get_line_user_id_by_customer_id(customer_id)
                print("invoice.payment_succeededイベント_wait_for_line_user_id関数_line_user_id:",line_user_id)
                if line_user_id is not None:
                    return line_user_id
                time.sleep(delay)
            raise ValueError("line_user_id is still None after 10 retries")
        
        customer_id = body['data']['object']['customer']
        print("invoice.payment_succeededイベントのcustomer_id:",customer_id)

        try:
            line_user_id = wait_for_line_user_id(customer_id, retries=5, delay=1)
        except ValueError as e:
            print("Error waiting for line_user_id:", e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'line_user_id is still None after 10 retries'})
            }

        product_id = get_product_id(event_type, body)
        print("invoice.payment_succeededイベントのproduct_id:",product_id)

        # 商品IDと顧客IDを使用して、メッセージの送信可能回数を更新
        try:
            db_accessor.update_message_count_by_product_id(customer_id, line_user_id, product_id)
            message = TextSendMessage(text="契約が更新されました。ステータスはステータスタブから確認できます。引き続きPicToLangをご活用ください。")
            line_bot_api.push_message(line_user_id, message)
        
        except ValueError as e:
            print("Error updating message count:", e)

        return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Successfully processed invoice.payment_succeeded event'})
    }


    elif event_type == 'customer.subscription.deleted': #解約時
        print("customer.subscription.deletedイベント発行")
        customer_id = body.get('data', {}).get('object', {}).get('customer')
        print("customer.subscription.deletedイベントのcustomer_id:", customer_id)
        line_user_id = db_accessor.get_line_user_id_by_customer_id(customer_id)

        # 顧客IDを使ってプランをfreeに更新
        try:
            db_accessor.update_plan_to_free_by_customer_id(customer_id)
            print("正常にユーザーのプランが'free'にアップデートされました")
            message = TextSendMessage(text="契約が解約されました。あなたはfreeユーザーにになりました。詳しい内容はメールからご確認ください。")
            line_bot_api.push_message(line_user_id, message)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Successfully processed customer.subscription.deleted event'})
            }
        except Exception as e:
            print("Error updating plan to free:", e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Error updating plan to free'})
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Event type {event_type} not handled'})
        }
