import json
from linebot.models import FlexSendMessage, QuickReply
from linebot import LineBotApi
from . import db_accessor
from . import line_api
from . import guard
from . import message_repository
from . import line_request_body_parser
from . import language_codes
import io
from . import const
from linebot import LineBotApi
from google.oauth2 import service_account
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import translate_v2

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
            QuickReplyButton(action=MessageAction(label="東京へ旅行", text="2泊3日で東京旅行の計画を立ててください")),
            QuickReplyButton(action=MessageAction(label="読書感想文", text="ハリーポッター賢者の石の読書感想文を描いてください")),
            QuickReplyButton(action=MessageAction(label="お金持ちになる", text="お金持ちになる方法を教えてください")),
            QuickReplyButton(action=MessageAction(label="上司へお礼メール", text="飲み会でお世話になった上司へのお礼メールを書いてください")),
            QuickReplyButton(action=MessageAction(label="日本の有名な観光名所", text="日本で有名な観光名所をいくつか教えてください")),
            QuickReplyButton(action=MessageAction(label="詳しく", text="もっと詳しく教えてください")),
            QuickReplyButton(action=MessageAction(label="英語学習", text="いくつかビジネスに必須な英単語とその　日本語訳をまとめたものを提示してください")),
            QuickReplyButton(action=MessageAction(label="研究テーマ", text="私にいくつか質問して、大学の研究テーマを一緒に考えてください")),
            QuickReplyButton(action=MessageAction(label="彼氏・彼女をなぐさめる", text="喧嘩した恋人と仲直りするためのメールを書いてください")),
            QuickReplyButton(action=MessageAction(label="仕事疲れた", text="仕事疲れたので、私を元気付けてください"))
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
            # QuickReplyButton(action=MessageAction(label="E-mail de agradecimento ao chefe", text="Escreva um e-mail de agradecimento ao meu chefe que cuidou de min na festa")),
            # QuickReplyButton(action=MessageAction(label="Atração turística famosa do Japão", text="Diga-me algumas atrações turísticas famosas no Japão.")),
            QuickReplyButton(action=MessageAction(label="Detalle", text="Cuéntame más en detalle")),
            QuickReplyButton(action=MessageAction(label="Aprender ingles", text="Proporcione una lista de algunas palabras esenciales del inglés comercial y sus traducciones al Español.")),
            QuickReplyButton(action=MessageAction(label="Buscar tema", text="Por favor, hágame algunas preguntas y elaboren juntos un tema de investigación para la universidad.")),
            # QuickReplyButton(action=MessageAction(label="Conforte seu namorado/namorada", text="Escreva um e-mail para fazer as pazes com seu amante que brigou")),
            QuickReplyButton(action=MessageAction(label="Cansado del trabajo", text="Estoy cansado del trabajo, así que anímame."))
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
            # QuickReplyButton(action=MessageAction(label="E-mail de agradecimento ao chefe", text="Escreva um e-mail de agradecimento ao meu chefe que cuidou de min na festa")),
            # QuickReplyButton(action=MessageAction(label="Atração turística famosa do Japão", text="Diga-me algumas atrações turísticas famosas no Japão.")),
            QuickReplyButton(action=MessageAction(label="Detalhe", text="Me conte mais em detalhes")),
            QuickReplyButton(action=MessageAction(label="Aprender inglês", text="Por favor, apresente uma lista de algumas palavras essenciais em inglês para negócios e suas traduções para o português")),
            QuickReplyButton(action=MessageAction(label="Tema de pesquisa", text="Por favor, faça-me algumas perguntas e crie um tópico de pesquisa para a universidade juntos.")),
            # QuickReplyButton(action=MessageAction(label="Conforte seu namorado/namorada", text="Escreva um e-mail para fazer as pazes com seu amante que brigou")),
            QuickReplyButton(action=MessageAction(label="Cansei do trabalho", text="Estou cansado do trabalho, então, por favor, me anime"))
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
    
    if message_count != 0:
        # Check if the event is a quick reply
        quick_reply_text = line_request_body_parser.get_quick_reply_text(event_body)
        if quick_reply_text is not None:
            prompt_text = quick_reply_text

        print("prompt_text:", prompt_text, "line_user_id:", line_user_id, "reply_token:", reply_token, "message_image_id:", message_image_id, "profile:", profile)

        # Get user's language
        user_language = language_codes.language_code_to_name[profile.language]
        print("user_language:", user_language)

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
        reply_message = "今月に送信できるメッセージの回数の上限に達しました。もっとメッセージを送りたい方は、アップグレードをご検討ください。"
        line_api.reply_message_for_line(reply_token, reply_message, None)

        basic_plan_url = f"https://buy.stripe.com/test_3cscNJfJK9RCcgM8ww?client_reference_id={line_user_id}"
        standard_plan_url = f"https://buy.stripe.com/test_3cscNJfJK9RCcgM8ww?client_reference_id={line_user_id}"
        premium_plan_url = f"https://buy.stripe.com/test_3cscNJfJK9RCcgM8ww?client_reference_id={line_user_id}"

        flex_message_contents = {
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
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "xl",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "none",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Basic Plan",
                                    "size": "sm",
                                    "wrap": True,
                                },
                                {
                                    "type": "text",
                                    "text": "85 yen and 25 messages per month",
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "none",
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#D7A9AA",  # Basic plan button color
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "Basic Plan",
                                        "uri": basic_plan_url
                                    }
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "none",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Standard Plan",
                                    "size": "sm",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": "160 yen and 100 messages per month",
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "none",
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#708090",  # Standard plan button color
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "Standard Plan",
                                        "uri": standard_plan_url
                                    }
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "none",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Premium Plan",
                                    "size": "sm",
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": "750 yen and Unlimited messages",
                                    "size": "sm",
                                    "wrap": True,
                                    "margin": "none",
                                },
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#D4AF37",  # Premium plan button color
                                    "height": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "Premium Plan",
                                        "uri": premium_plan_url
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

        flex_message = FlexSendMessage(alt_text='Choose a plan', contents=flex_message_contents)

        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        line_bot_api.push_message(line_user_id, flex_message)