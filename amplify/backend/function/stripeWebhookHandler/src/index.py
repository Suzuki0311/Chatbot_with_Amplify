print("index.pyは起動している")
import json
import const
import db_accessor
import stripe
from botocore.exceptions import ClientError
import time
from linebot import LineBotApi, WebhookHandler
from linebot.models import FlexSendMessage, QuickReply, QuickReplyButton, MessageAction,TextSendMessage,TemplateSendMessage, ConfirmTemplate
from datetime import datetime

stripe.api_key = const.STRIPE_API_KEY
endpoint_secret = const.endpoint_secret

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

def get_next_update_date(customer_id):
    subscriptions = stripe.Subscription.list(customer=customer_id)

    for subscription in subscriptions:
        if subscription["status"] == "active":
            next_update_date = subscription["current_period_end"]
            return datetime.fromtimestamp(next_update_date).strftime('%Y-%m-%dT%H:%M:%S%z')
    return None

def create_quick_reply_buttons(user_language):
    if user_language == 'Japanese':
        return [
            QuickReplyButton(action=MessageAction(label="日本語に翻訳", text="上記を日本語に翻訳してください")),
            QuickReplyButton(action=MessageAction(label="英語に翻訳", text="上記を英語に翻訳してください")),
            QuickReplyButton(action=MessageAction(label="1週間の献立", text="1週間の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="仕事疲れた", text="仕事疲れたので、私を元気付けてください")),
            QuickReplyButton(action=MessageAction(label="読書感想文", text="ハリーポッター賢者の石の読書感想文を描いてください")),
            QuickReplyButton(action=MessageAction(label="お金持ちになる", text="お金持ちになる方法を教えてください")),
            QuickReplyButton(action=MessageAction(label="上司へお礼メール", text="飲み会でお世話になった上司へのお礼メールを書いてください")),
            QuickReplyButton(action=MessageAction(label="日本の有名な観光名所", text="日本で有名な観光名所をいくつか教えてください")),
            QuickReplyButton(action=MessageAction(label="英語学習", text="いくつかビジネスに必須な英単語とその日本語訳をまとめたものを提示してください")),
            QuickReplyButton(action=MessageAction(label="ステータス", text="今のステータスを教えてください")),
            QuickReplyButton(action=MessageAction(label="アップグレード", text="アップグレードしたいです")),
            QuickReplyButton(action=MessageAction(label="お問い合わせ", text="お問い合わせ")),
            QuickReplyButton(action=MessageAction(label="解約", text="解約したいです"))
    ]

    elif user_language == 'Spanish':
        return  [
            QuickReplyButton(action=MessageAction(label="Traducción Española", text="Traduce lo anterior al Español.")),
            QuickReplyButton(action=MessageAction(label="Traducir inglés", text="Traduce lo anterior al inglés.")),
            QuickReplyButton(action=MessageAction(label="Menú de 1 semana", text="Sugerir un menú para la semana.")),
            QuickReplyButton(action=MessageAction(label="Viajar a Tokyo", text="Planea para mí un viaje a Tokyo de 3 días y 2 noches")),
            QuickReplyButton(action=MessageAction(label="Reporte de lectura", text="Diseñar un informe de libro para la piedra filosofal de Harry Potter")),
            QuickReplyButton(action=MessageAction(label="Hacerse rico", text="Dime como hacerme rico")),
            QuickReplyButton(action=MessageAction(label="Detalle", text="Cuéntame más en detalle")),
            QuickReplyButton(action=MessageAction(label="Aprender ingles", text="Proporcione una lista de algunas palabras esenciales del inglés comercial y sus traducciones al Español.")),
            QuickReplyButton(action=MessageAction(label="Estado", text="Dime el estado.")),
            QuickReplyButton(action=MessageAction(label="Cansado del trabajo", text="Estoy cansado del trabajo, así que anímame.")),
            QuickReplyButton(action=MessageAction(label="Actualizar", text="Quiero actualizar mi aplicación.")),
            QuickReplyButton(action=MessageAction(label="contacto", text="contacto")),
            QuickReplyButton(action=MessageAction(label="Cancelar", text="Quiero cancelar la aplicación"))
    ]

    elif user_language == 'Portuguese':
        return  [
            QuickReplyButton(action=MessageAction(label="Traduzir portugues", text="Traduza o acima para o portugues")),
            QuickReplyButton(action=MessageAction(label="Traduzir inglês", text="Traduza o acima para o inglês")),
            QuickReplyButton(action=MessageAction(label="Cardápio de 1 semana", text="Sugira um menu para a semana")),
            QuickReplyButton(action=MessageAction(label="Viajar para Tokyo", text="Planeje para min uma viagem para Tokyo por 3 dias e 2 noites")),
            QuickReplyButton(action=MessageAction(label="Relatório de leitura", text="Desenhe um relatório de livro para a Pedra Filosofal de Harry Potter")),
            QuickReplyButton(action=MessageAction(label="Ficar rico", text="Me diga como ficar rico")),
            QuickReplyButton(action=MessageAction(label="Detalhe", text="Me conte mais em detalhes")),
            QuickReplyButton(action=MessageAction(label="Aprender inglês", text="Por favor, apresente uma lista de algumas palavras essenciais em inglês para negócios e suas traduções para o português")),
            QuickReplyButton(action=MessageAction(label="Estado", text="Diga-me o estado.")),
            QuickReplyButton(action=MessageAction(label="Cansei do trabalho", text="Estou cansado do trabalho, então, por favor, me anime")),
            QuickReplyButton(action=MessageAction(label="Atualizar", text="Eu quero atualizar meu aplicativo")),
            QuickReplyButton(action=MessageAction(label="Contato conosco", text="Contato conosco")),
            QuickReplyButton(action=MessageAction(label="Cancelar", text="Quero cancelar o aplicativo"))
    ]

    elif user_language == 'Vietnamese':
        return [
            QuickReplyButton(action=MessageAction(label="Dịch sang Tiếng Việt", text="Dịch phía trên sang tiếng Việt")),
            QuickReplyButton(action=MessageAction(label="Dịch sang Tiếng Anh", text="Dịch phía trên sang tiếng Anh")),
            QuickReplyButton(action=MessageAction(label="Thực đơn 1 tuần", text="Đề xuất thực đơn cho tuần này")),
            QuickReplyButton(action=MessageAction(label="Đi Tokyo", text="Lên kế hoạch đi Tokyo 3 ngày 2 đêm")),
            QuickReplyButton(action=MessageAction(label="Báo cáo sách", text="Viết báo cáo sách Harry Potter và Hòn Đá Phù Thủy")),
            QuickReplyButton(action=MessageAction(label="Giàu có", text="Hãy nói cách trở nên giàu có")),
            QuickReplyButton(action=MessageAction(label="Chi tiết", text="Kể thêm chi tiết")),
            QuickReplyButton(action=MessageAction(label="Học Tiếng Anh", text="Giới thiệu danh sách các từ tiếng Anh cần thiết cho kinh doanh và bản dịch tiếng Việt")),
            QuickReplyButton(action=MessageAction(label="Trạng thái", text="Cho tôi biết trạng thái")),
            QuickReplyButton(action=MessageAction(label="Mệt mỏi", text="Tôi mệt mỏi vì công việc, hãy làm tôi vui")),
            QuickReplyButton(action=MessageAction(label="Cập nhật", text="Tôi muốn cập nhật ứng dụng")),
            QuickReplyButton(action=MessageAction(label="Liên hệ", text="Liên hệ với chúng tôi")),
            QuickReplyButton(action=MessageAction(label="Hủy bỏ", text="Tôi muốn hủy ứng dụng"))
    ]

    elif user_language == 'Tagalog':
        return [
            QuickReplyButton(action=MessageAction(label="Isalin sa Tagalog", text="Isalin ang itaas sa Tagalog")),
            QuickReplyButton(action=MessageAction(label="Isalin sa Ingles", text="Isalin ang itaas sa Ingles")),
            QuickReplyButton(action=MessageAction(label="Menu ng 1 linggo", text="Magmungkahi ng menu para sa linggo")),
            QuickReplyButton(action=MessageAction(label="Biyaheng Tokyo", text="Magplano ng 3 araw at 2 gabi sa Tokyo")),
            QuickReplyButton(action=MessageAction(label="Ulat ng pagbabasa", text="Gumawa ng aklat na ulat para sa Harry Potter at Philosopher's Stone")),
            QuickReplyButton(action=MessageAction(label="Yaman", text="Sabihin kung paano yumaman")),
            QuickReplyButton(action=MessageAction(label="Detalye", text="Kwento ng mas detalyado")),
            QuickReplyButton(action=MessageAction(label="Aralin Ingles", text="Pakilala ng listahan ng ilang mahalagang salita sa Ingles para sa negosyo at ang pagsasalin nito sa Tagalog")),
            QuickReplyButton(action=MessageAction(label="Status", text="Sabihin ang kasalukuyang status")),
            QuickReplyButton(action=MessageAction(label="Pagod sa trabaho", text="Pagod ako sa trabaho, pakipasaya ako")),
            QuickReplyButton(action=MessageAction(label="I-update", text="Gusto kong i-update ang aking app")),
            QuickReplyButton(action=MessageAction(label="Makipag-ugnay", text="Makipag-ugnay sa amin")),
            QuickReplyButton(action=MessageAction(label="Kanselahin", text="Gusto kong kanselahin ang app"))
    ]
    else:
        return [
            QuickReplyButton(action=MessageAction(label="Translate English", text="Translate the above to English")),
            QuickReplyButton(action=MessageAction(label="Translate other", text="Translate the above to another language")),
            QuickReplyButton(action=MessageAction(label="1-week menu", text="Suggest a menu for the week")),
            QuickReplyButton(action=MessageAction(label="Tokyo trip", text="Plan a 3-day, 2-night trip to Tokyo")),
            QuickReplyButton(action=MessageAction(label="Reading report", text="Write a book report for Harry Potter and the Philosopher's Stone")),
            QuickReplyButton(action=MessageAction(label="Get rich", text="Tell me how to get rich")),
            QuickReplyButton(action=MessageAction(label="Details", text="Tell me more in detail")),
            QuickReplyButton(action=MessageAction(label="Learn English", text="Please introduce a list of some essential English words for business and their translations")),
            QuickReplyButton(action=MessageAction(label="Status", text="Tell me the status.")),
            QuickReplyButton(action=MessageAction(label="Tired from work", text="I am tired from work, so please cheer me up")),
            QuickReplyButton(action=MessageAction(label="Upgrade", text="I want to upgrade my app")),
            QuickReplyButton(action=MessageAction(label="Contact us", text="Contact us")),
            QuickReplyButton(action=MessageAction(label="Cancel", text="I want to cancel the app"))
    ]


def handler(event, context):
    # Extract the payload from the event and the Stripe signature from the headers
    payload = event['body']
    sig_header = event['headers']['Stripe-Signature']
    stripe_event = None

    try:
        stripe_event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return {'statusCode': 400, 'body': json.dumps('Invalid payload')}
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return {'statusCode': 400, 'body': json.dumps('Invalid signature')}
    
    print('received event:')
    print(event)
    
    # Parse the 'body' key
    # body = json.loads(event['body'])
    # body = json.loads(stripe_event)

    # Get the 'type' key from the parsed body
    event_type = stripe_event.get('type', '')

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

        next_update_date = get_next_update_date(customer_id)
        
        product_id = get_product_id(event_type, body)
        print("invoice.payment_succeededイベントのproduct_id:",product_id)

        user_language = db_accessor.get_user_language_by_line_user_id(line_user_id)

        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        # 商品IDと顧客IDを使用して、メッセージの送信可能回数を更新
        try:
            db_accessor.update_message_count_by_product_id(customer_id, line_user_id, product_id, next_update_date)
            if user_language == 'Portuguese':
                message = TextSendMessage(text='Seu plano foi atualizado. Você pode verificar o status atualizado na guia "Estado".',quick_reply=quick_reply)
            elif user_language == 'Spanish':
                message = TextSendMessage(text='Su plan ha sido actualizado. Puede verificar el estado actualizado en la pestaña "Estado".',quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                message = TextSendMessage(text='Na-update na ang iyong plano. Maaari mong tingnan ang na-update na status sa tab na "Status".',quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                message = TextSendMessage(text='Kế hoạch của bạn đã được cập nhật. Bạn có thể kiểm tra trạng thái cập nhật trong tab "Trạng thái".',quick_reply=quick_reply)
            elif user_language == 'Japanese':
                message = TextSendMessage(text='あなたのプランを更新しました。更新されたステータスは、"ステータス"タブから確認できます。ぜひ思う存分PicToLangをご活用ください。',quick_reply=quick_reply)
            else:
                message = TextSendMessage(text='Your plan has been updated. You can check the updated status in the "Status" tab.',quick_reply=quick_reply)
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
        user_language = db_accessor.get_user_language_by_line_user_id(line_user_id)

        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        # 顧客IDを使ってプランをfreeに更新
        try:
            db_accessor.update_plan_to_free_by_customer_id(customer_id)
            print("正常にユーザーのプランが'free'にアップデートされました")

            if user_language == 'Portuguese':
                message = TextSendMessage(text="O cancelamento está completo. Agora você é um usuário gratuito. Obrigado por usar o PicToLang.",quick_reply=quick_reply)
            elif user_language == 'Spanish':
                message = TextSendMessage(text="La cancelación está completa. Ahora eres un usuario gratuito. Gracias por usar PicToLang.",quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                message = TextSendMessage(text="Kumpleto na ang pagkansela. Isa ka na ngayong libreng user. Salamat sa paggamit ng PicToLang.",quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                message = TextSendMessage(text="Việc hủy bỏ đã hoàn tất. Bây giờ bạn là người dùng miễn phí. Cảm ơn bạn đã sử dụng PicToLang.",quick_reply=quick_reply)
            elif user_language == 'Japanese':
                message = TextSendMessage(text="解約が完了しました。あなたはfreeユーザーになりました。PicToLangを使い頂きありがとうございました。",quick_reply=quick_reply)
            else:
                message = TextSendMessage(text="Cancellation is complete. You are now a free user. Thank you for using PicToLang.",quick_reply=quick_reply)

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
    elif event_type == 'invoice.payment_failed': # 支払い失敗時
        print("invoice.payment_failedイベント発行")
        customer_id = body['data']['object']['customer']
        print("invoice.payment_failedイベントのcustomer_id:", customer_id)

        line_user_id = db_accessor.get_line_user_id_by_customer_id(customer_id)
        if line_user_id is None:
            print("Error: line_user_id not found for customer_id:", customer_id)
        else:
            user_language = db_accessor.get_user_language_by_line_user_id(line_user_id)

            quick_reply_buttons = create_quick_reply_buttons(user_language)
            quick_reply = QuickReply(items=quick_reply_buttons)

            if user_language == 'Portuguese':
                message = TextSendMessage(text="Seu pagamento falhou. Verifique suas informações de pagamento.",quick_reply=quick_reply)
            elif user_language == 'Spanish':
                message = TextSendMessage(text="Su pago falló. Verifique su información de pago.",quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                message = TextSendMessage(text="Nabigo ang iyong pagbabayad. Suriin ang iyong impormasyon sa pagbabayad.",quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                message = TextSendMessage(text="Thanh toán của bạn không thành công. Kiểm tra thông tin thanh toán của bạn.",quick_reply=quick_reply)
            elif user_language == 'Japanese':
                message = TextSendMessage(text="お支払いに失敗しました。お手数ですが、お支払い情報をご確認ください。",quick_reply=quick_reply)
            else:
                message = TextSendMessage(text="Your payment failed. Check your payment information.",quick_reply=quick_reply)
            line_bot_api.push_message(line_user_id, message)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Successfully processed invoice.payment_failed event'})
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Event type {event_type} not handled'})
        }
    
