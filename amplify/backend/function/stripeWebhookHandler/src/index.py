print("index.pyは起動している")
import json
import const
import db_accessor
import stripe

stripe.api_key = const.STRIPE_API_KEY

def get_product_id_from_checkout_session_completed(event_data):
    session_id = event_data['data']['object']['id']
    session = stripe.checkout.Session.retrieve(session_id)
    line_items = stripe.checkout.Session.list_line_items(session_id)
    product_id = line_items['data'][0]['price']['product']

    return product_id

def handler(event, context):
    print('received event:')
    print(event)
    
    # Parse the 'body' key
    body = json.loads(event['body'])

    # Get the 'type' key from the parsed body
    event_type = body.get('type', '')

    if event_type == 'checkout.session.completed': #初回購入時
        session = body['data']['object']

        line_user_id = session.get('client_reference_id')
        print("line_user_id_client_reference_id:", line_user_id)

        customer_id = session['customer']
        print("customer_id:", customer_id)

        product_id = get_product_id_from_checkout_session_completed(body)
        print("product_id:", product_id)

        items = db_accessor.search_customer_in_table(customer_id)
        if not items:  # リストが空の場合
            print("顧客IDがテーブルに存在しません。")
            db_accessor.update_customer_id_by_client_reference_id(line_user_id, customer_id)

        db_accessor.update_message_count_by_product_id(customer_id, line_user_id, product_id)
        print("正常にユーザーの回数がアップデートされました")
    