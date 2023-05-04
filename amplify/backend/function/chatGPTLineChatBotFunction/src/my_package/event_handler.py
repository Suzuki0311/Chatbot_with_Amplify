import json
from linebot.models import FlexSendMessage, QuickReply, QuickReplyButton, MessageAction,TextSendMessage,TemplateSendMessage, ConfirmTemplate
from linebot import LineBotApi
from . import db_accessor
from . import line_api
from . import message_repository
from . import line_request_body_parser
from . import language_codes
from . import flex_message_contents
import io
from . import const
from linebot.exceptions import LineBotApiError
from google.oauth2 import service_account
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import translate_v2
import stripe
import time

def send_flex_message(plan, line_user_id, quick_reply):
            basic_plan_url = f"{const.PRODUCT_URL_BASIC}?client_reference_id={line_user_id}"
            standard_plan_url = f"{const.PRODUCT_URL_STANDARD}?client_reference_id={line_user_id}"
            premium_plan_url = f"{const.PRODUCT_URL_PREMIUM}?client_reference_id={line_user_id}"

            basic_plan_component = flex_message_contents.basic_plan_component(basic_plan_url)
            standard_plan_component = flex_message_contents.standard_plan_component(standard_plan_url)
            premium_plan_component = flex_message_contents.premium_plan_component(premium_plan_url)

            if plan == "free":
                flex_message_reply = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "You've reached your message limit.",
                            "weight": "bold",
                            "size": "xl"
                        },
                        basic_plan_component,
                        standard_plan_component,
                        premium_plan_component
                    ]
                }
            }
            elif plan == "basic":
                flex_message_reply = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "You've reached your message limit, please upgrade your plan",
                            "weight": "bold",
                            "size": "xl"
                        },
                        standard_plan_component,
                        premium_plan_component
                    ]
                }
            }
            elif plan == "standard":
                flex_message_reply = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "You've reached your message limit, please upgrade your plan",
                            "weight": "bold",
                            "size": "xl"
                        },
                        premium_plan_component
                    ]
                }
            }


            flex_message = FlexSendMessage(alt_text='Choose a plan', contents=flex_message_reply,quick_reply=quick_reply)
            return flex_message

def send_flex_message_upgrade(quick_reply):
            basic_plan_component = flex_message_contents.basic_plan_component_upgrade()
            standard_plan_component = flex_message_contents.standard_plan_component_upgrade()
            premium_plan_component = flex_message_contents.premium_plan_component_upgrade()

            flex_message_reply = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "You've reached your message limit.",
                                    "weight": "bold",
                                    "size": "xl"
                                },
                                basic_plan_component,
                                standard_plan_component,
                                premium_plan_component
                            ]
                        }
                    }
            
            flex_message = FlexSendMessage(alt_text='Choose a plan', contents=flex_message_reply,quick_reply=quick_reply)
            return flex_message


def extract_info_from_event_body(event_body):
    prompt_text = line_request_body_parser.get_prompt_text(event_body)
    line_user_id = line_request_body_parser.get_line_user_id(event_body)
    reply_token = line_request_body_parser.get_reply_token(event_body)
    message_image_id = line_request_body_parser.get_image_content(event_body)
    line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
    profile = line_bot_api.get_profile(line_user_id)

    return prompt_text, line_user_id, reply_token, message_image_id, profile

def process_image(message_image_id):
    line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
    message_image_content = line_bot_api.get_message_content(message_image_id)
    image_bytes = io.BytesIO(message_image_content.content)
    service_account_info = json.loads(const.GOOGLE_APPLICATION_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.Image(content=image_bytes.getvalue())
    response = client.document_text_detection(image=image)
    target_sentence = response.full_text_annotation.text
    translate_client = translate_v2.Client(credentials=credentials)
    text_language = translate_client.detect_language(target_sentence)
    text_language = language_codes.language_code_to_name[text_language['language']]
    prompt_text = target_sentence

    return prompt_text, text_language

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
            QuickReplyButton(action=MessageAction(label="彼氏・彼女をなぐさめる", text="喧嘩した恋人と仲直りするためのメールを書いてください")),
            QuickReplyButton(action=MessageAction(label="アップグレード", text="アップグレードしたいです")),
            QuickReplyButton(action=MessageAction(label="お問い合わせ", text="お問い合わせ")),
            QuickReplyButton(action=MessageAction(label="解約", text="解約したいです"))
    ]
    elif user_language == 'English':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
    ]
    elif user_language == 'Chinese':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
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
            QuickReplyButton(action=MessageAction(label="Buscar tema", text="Por favor, hágame algunas preguntas y elaboren juntos un tema de investigación para la universidad.")),
            QuickReplyButton(action=MessageAction(label="Cansado del trabajo", text="Estoy cansado del trabajo, así que anímame.")),
            QuickReplyButton(action=MessageAction(label="Actualizar", text="Quiero actualizar mi aplicación.")),
            QuickReplyButton(action=MessageAction(label="contacto", text="contacto")),
            QuickReplyButton(action=MessageAction(label="Cancelar", text="Quiero cancelar la aplicación"))
    ]
    elif user_language == 'French':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
    ]
    elif user_language == 'German':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
    ]
    elif user_language == 'Italian':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
    ]
    elif user_language == 'Korean':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
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
            QuickReplyButton(action=MessageAction(label="Tema de pesquisa", text="Por favor, faça-me algumas perguntas e crie um tópico de pesquisa para a universidade juntos.")),
            QuickReplyButton(action=MessageAction(label="Cansei do trabalho", text="Estou cansado do trabalho, então, por favor, me anime")),
            QuickReplyButton(action=MessageAction(label="Atualizar", text="Eu quero atualizar meu aplicativo")),
            QuickReplyButton(action=MessageAction(label="Contato conosco", text="Contato conosco")),
            QuickReplyButton(action=MessageAction(label="Cancelar", text="Quero cancelar o aplicativo"))
    ]
    elif user_language == 'Thai':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
    ]
    elif user_language == 'Vietnamese':
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
    ]


 # 顧客IDからサブスクリプションIDを取得
def get_subscription_id(customer_id):
    subscriptions = stripe.Subscription.list(customer=customer_id, limit=1)
    if subscriptions["data"]:
        subscription_id = subscriptions["data"][0]["id"]
        return subscription_id
    else:
        return None

def handle_follow_event(event_body):
    # Extract the user ID and reply token
    line_user_id = event_body['events'][0]['source']['userId']
    reply_token = event_body['events'][0]['replyToken']

    # Check if the user exists in DynamoDB
    user_exists = db_accessor.check_line_user_id_exists(line_user_id)

    # If the user doesn't exist in DynamoDB, insert their data
    if user_exists == "No":
        db_accessor.insert_data(line_user_id)
        welcome_message = "友達登録ありがとうございます。PicToLangの使い方やお問い合わせの仕方について、下記リンクから参照ください。また現時点であなたは月に7回のメッセージを送ることができるFreeユーザーです。それ以上お使いになりたい方は、下のタブのアップデート欄からアップデートください。"
    else:
        user_data = db_accessor.get_line_user_data(line_user_id)
        plan = user_data['plan']
        message_count = user_data['message_count']
        welcome_message = f"再び友達登録していただき、ありがとうございます。あなたは現在、{plan}ユーザーであり、今月は残り{message_count}回メッセージを送ることができます。引き続きどうぞよろしくお願いします。"

    # Reply the welcome message using the LineBotApi instance
    line_api.reply_message_for_line(reply_token, welcome_message, None)  # Consider removing QuickReply or using a different function for sending the message

def handle_message_event(event_body):
    # Extract necessary information from event_body
    prompt_text, line_user_id, reply_token, message_image_id, profile = extract_info_from_event_body(event_body)
    message_count = db_accessor.get_current_message_count(line_user_id)
    print("現在のメッセージ可能回数:", message_count)
    quick_reply_text = line_request_body_parser.get_quick_reply_text(event_body)
    stripe.api_key = const.STRIPE_API_KEY

    if quick_reply_text is not None:
        prompt_text = quick_reply_text

    print("prompt_text:", prompt_text, "line_user_id:", line_user_id, "reply_token:", reply_token, "message_image_id:", message_image_id, "profile:", profile)

    # Get user's language
    user_language = language_codes.language_code_to_name[profile.language]
    print("user_language:", user_language)

    if prompt_text == "Quiero actualizar mi aplicación." or prompt_text == "Eu quero atualizar meu aplicativo" or prompt_text == "アップグレードしたいです" :
        plan = db_accessor.get_user_plan(line_user_id)
        print("plan:",plan)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)
        flex_message = send_flex_message_upgrade(quick_reply)
        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

        from linebot.exceptions import LineBotApiError
        try:

            text_message = TextSendMessage(text=f"あなたのプランは{plan}です。下記のボタンからアップグレードもしくはダウングレードしたいプランを選択してください。", quick_reply=quick_reply)
            line_bot_api.reply_message(reply_token, [text_message, flex_message])
            
        except LineBotApiError as e:
            print("Error:", e)

    elif prompt_text == "Contato conosco" or prompt_text == "contacto" or prompt_text == "お問い合せ" :
         # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        from linebot.exceptions import LineBotApiError
        try:
            text_message = TextSendMessage(
                            text="下記リンクから必要事項を記入して、送信してください\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new",
                            quick_reply=quick_reply
                        )
            line_bot_api.reply_message(reply_token, text_message)
            # line_bot_api.reply_message(reply_token, [text_message, flex_message])
        except LineBotApiError as e:
            print("Error:", e)

    elif prompt_text == "Quero cancelar o aplicativo" or prompt_text == "Quiero cancelar la aplicación" or prompt_text == "解約したいです" :
        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)
        from linebot.exceptions import LineBotApiError
        try:
            actions = [
                        MessageAction(label="はい", text="はい、私は本当に解約します。"),
                        MessageAction(label="いいえ", text="いいえ"),
                      ]
            # Create a ConfirmTemplate
            confirm_template = ConfirmTemplate(text="本当に解約しますか？", actions=actions)

            # Create a TemplateSendMessage with the ConfirmTemplate
            message = TemplateSendMessage(alt_text="this is a confirm template", template=confirm_template)

            # text_message = TextSendMessage(text="下記リンクから解約を行ってください", quick_reply=quick_reply)
            line_bot_api.reply_message(reply_token, message)
            # line_bot_api.reply_message(line_user_id, flex_message)
            # line_bot_api.reply_message(reply_token, [text_message, flex_message])
        except LineBotApiError as e:
            print("Error:", e)
    elif prompt_text == "はい、私は本当に解約します。":

        # サブスクリプションをキャンセル
        def cancel_subscription(subscription_id):
            canceled_subscription = stripe.Subscription.delete(subscription_id)
            return canceled_subscription
        
        customer_id = db_accessor.get_customer_id_by_line_user_id(line_user_id)
        print("サブスクリプションをキャンセル_customer_id:",customer_id)

        subscription_id = get_subscription_id(customer_id)

         # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        if subscription_id:
            print(f"Subscription ID: {subscription_id}")

            # サブスクリプションをキャンセル
            canceled_subscription = cancel_subscription(subscription_id)
            print(f"Canceled subscription: {canceled_subscription['id']}")

            text_message = TextSendMessage(text="解約が完了しました。詳細はメールにてご確認ください。", quick_reply=quick_reply)

            # Push the message to the user
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

            from linebot.exceptions import LineBotApiError
            try:
                line_bot_api.reply_message(reply_token, text_message)
            except LineBotApiError as e:
                print("Error:", e)
        else:
            print("No active subscription found for this customer.")

            text_message = TextSendMessage(text="あなたのプランを見つけることができませんでした。以下URLよりお問合せください。", quick_reply=quick_reply)

            # Push the message to the user
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            from linebot.exceptions import LineBotApiError
            try:
                line_bot_api.reply_message(reply_token, text_message)
            except LineBotApiError as e:
                print("Error:", e)
    
    elif prompt_text == "I want to subscribe to the Basic Plan" or prompt_text == "I want to subscribe to the Standard Plan" or prompt_text == "I want to subscribe to the Premium Plan":
        if prompt_text == "I want to subscribe to the Basic Plan":
            plan = "basic"
            send_text = "月額80で月に100回メッセージを送ることができます。"
        elif prompt_text == "I want to subscribe to the Standard Plan":
            plan = "standard"
            send_text = "月額230で月に300回メッセージを送ることができます。"
        elif prompt_text == "I want to subscribe to the Premium Plan":
            plan = "premium"
            send_text = "月額750で無制限にメッセージを送ることができます。"

        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)
        from linebot.exceptions import LineBotApiError
        try:
            actions = [
                        MessageAction(label="はい", text=f"はい。私は{plan}を契約します。"),
                        MessageAction(label="いいえ", text="いいえ"),
                      ]
            # Create a ConfirmTemplate
            confirm_template = ConfirmTemplate(text=f"{plan}は、{send_text}契約を確定させたい場合は、以下の「はい」をクリックしてください", actions=actions)

            # Create a TemplateSendMessage with the ConfirmTemplate
            message = TemplateSendMessage(alt_text="this is a confirm template", template=confirm_template)

            line_bot_api.reply_message(reply_token, message)

        except LineBotApiError as e:
            print("Error:", e)
    elif prompt_text == "はい。私はbasicを契約します。" or prompt_text == "はい。私はstandardを契約します。"or prompt_text == "はい。私はpremiumを契約します。":

        # def find_pending_invoice(customer_id, subscription_id, retries=3, delay=2):
        #     for _ in range(retries):
        #         pending_invoices = stripe.Invoice.list(
        #             customer=customer_id,
        #             subscription=subscription_id,
        #             status="open",
        #         )
        #         for invoice in pending_invoices.data:
        #             if invoice.subscription == subscription_id:
        #                 return invoice
        #         time.sleep(delay)
        #     return None
        
        def find_pending_invoice(customer_id, retries=3, delay=1):
            for _ in range(retries):
                pending_invoices = stripe.Invoice.list(
                    customer=customer_id,
                    status="open",
                )
                print("pending_invoices:",pending_invoices)
                for invoice in pending_invoices.data:
                    return invoice
                time.sleep(delay)
            return None
        
        customer_id = db_accessor.get_customer_id_by_line_user_id(line_user_id)
        subscription_id = get_subscription_id(customer_id)

        if prompt_text == "はい。私はbasicを契約します。":
            new_plan_id = const.PRICE_ID_BASIC
        elif prompt_text == "はい。私はstandardを契約します。":
            new_plan_id = const.PRICE_ID_STANDARD
        elif prompt_text == "はい。私はpremiumを契約します。":
            new_plan_id = const.PRICE_ID_PREMIUM

        try:
            # サブスクリプションを取得
            subscription = stripe.Subscription.retrieve(subscription_id)
            print("# サブスクリプションを取得_subscription:",subscription)

            # 現在のサブスクリプションに紐づく最初のアイテムを取得
            subscription_item_id = subscription["items"]["data"][0]["id"]
            print("subscription_item_id:",subscription_item_id)

            # サブスクリプションの変更を確定し、プロレーション料金を適用
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                items=[{"id": subscription_item_id, "price": new_plan_id}],
                proration_behavior="create_prorations",
            )
            print("updated_subscription:", updated_subscription)

            # プロレーション料金が含まれる未払いのインボイスを取得
            # pending_invoice = find_pending_invoice(customer_id, subscription_id)
            pending_invoice = find_pending_invoice(customer_id)

            if pending_invoice:
                print("pending_invoice:", pending_invoice)
                stripe.Invoice.pay(pending_invoice.id) # 生成されたインボイスを即時支払い
            else:
                print("No pending invoice found after retries")

            # # 現在のサブスクリプションをキャンセル
            # canceled_subscription = stripe.Subscription.delete(subscription_id)
            # print("canceled_subscription:", canceled_subscription)

            # # 新しいサブスクリプションを作成（新しい商品IDを指定）
            # new_subscription = stripe.Subscription.create(
            #     customer=customer_id,
            #     items=[{"price": new_plan_id}],
            #     expand=["latest_invoice.payment_intent"],
            # )
            # print("new_subscription:", new_subscription)

        except Exception as e:
            print(f"Error upgrading subscription: {e}")
            return None

    else:
        if message_count != 0:
            # Process image if present
            if message_image_id is not None:
                prompt_text, text_language = process_image(message_image_id)
                print("The prompt_text when image is present:", prompt_text, "text_language:", text_language)
            else:
                text_language = None

            # Check if the event is a message type and is of text type
            if prompt_text is None or line_user_id is None or reply_token is None:
                raise Exception('Elements of the event body are not found.')

            # Create the completed text by Chat-GPT 3.5 turbo
            completed_text = message_repository.create_completed_text(line_user_id, prompt_text, message_image_id, text_language, user_language)
            print("completed_text:", completed_text)

            # Create quick reply buttons
            quick_reply_buttons = create_quick_reply_buttons(user_language)
            quick_reply = QuickReply(items=quick_reply_buttons)

            # Reply the message using the LineBotApi instance with quick replies
            line_api.reply_message_for_line(reply_token, completed_text, quick_reply)
            db_accessor.decrement_message_count(line_user_id, message_count)
        else:
            # reply_message = "今月に送信できるメッセージの回数の上限に達しました。もっとメッセージを送りたい方は、アップグレードをご検討ください。"
            # line_api.reply_message_for_line(reply_token, reply_message, None)

            # Create quick reply buttons
            quick_reply_buttons = create_quick_reply_buttons(user_language)
            quick_reply = QuickReply(items=quick_reply_buttons)

            plan = db_accessor.get_user_plan(line_user_id)
            print("plan:",plan)
            if plan == "free":
                flex_message = send_flex_message(plan, line_user_id, quick_reply)
            else:
                flex_message = send_flex_message_upgrade(quick_reply)

            text_message = TextSendMessage(text=f"今月に送信できるメッセージの回数の上限に達しました。あなたのプランは{plan}です。もっとメッセージを送りたい方は、下記のボタンからアップグレードしたいプランを選択してください。", quick_reply=quick_reply)
 
            # Push the message to the user
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            from linebot.exceptions import LineBotApiError
            try:
                line_bot_api.reply_message(reply_token, [text_message, flex_message])
            except LineBotApiError as e:
                print("Error:", e)