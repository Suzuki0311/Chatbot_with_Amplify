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

def send_flex_message(plan, line_user_id, quick_reply,user_language):
            basic_plan_url = f"{const.PRODUCT_URL_BASIC}?client_reference_id={line_user_id}"
            standard_plan_url = f"{const.PRODUCT_URL_STANDARD}?client_reference_id={line_user_id}"
            premium_plan_url = f"{const.PRODUCT_URL_PREMIUM}?client_reference_id={line_user_id}"

            basic_plan_component = flex_message_contents.basic_plan_component(basic_plan_url,user_language)
            standard_plan_component = flex_message_contents.standard_plan_component(standard_plan_url,user_language)
            premium_plan_component = flex_message_contents.premium_plan_component(premium_plan_url,user_language)

            if user_language == 'Portuguese':
                text_below = "Lista de planos"
            elif user_language == 'Spanish':
                text_below = "Lista de planes"
            elif user_language == 'Tagalog':
                text_below = "Listahan ng Plano"
            elif user_language == 'Vietnamese':
                text_below = "Danh sách kế hoạch"
            elif user_language == 'Japanese':
                text_below = "プラン一覧"
            else:
                text_below = "Plan List"

            flex_message_reply = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text_below,
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

def send_flex_message_upgrade(plan,quick_reply,user_language):
            basic_plan_component = flex_message_contents.basic_plan_component_upgrade(user_language)
            standard_plan_component = flex_message_contents.standard_plan_component_upgrade(user_language)
            premium_plan_component = flex_message_contents.premium_plan_component_upgrade(user_language)

            if user_language == 'Portuguese':
                text_below = "Lista de planos"
            elif user_language == 'Spanish':
                text_below = "Lista de planes"
            elif user_language == 'Tagalog':
                text_below = "Listahan ng Plano"
            elif user_language == 'Vietnamese':
                text_below = "Danh sách kế hoạch"
            elif user_language == 'Japanese':
                text_below = "プラン一覧"
            else:
                text_below = "Plan List"

            if plan == "basic":
                flex_message_reply = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text_below,
                            "weight": "bold",
                            "size": "xl"
                        },
                        # basic_plan_component,
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
                            "text": text_below,
                            "weight": "bold",
                            "size": "xl"
                        },
                        basic_plan_component,
                        # standard_plan_component,
                        premium_plan_component
                    ]
                }
            }
            
            elif plan == "premium":
                flex_message_reply = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text_below,
                            "weight": "bold",
                            "size": "xl"
                        },
                        basic_plan_component,
                        standard_plan_component,
                        # premium_plan_component
                    ]
                }
            }
            
            flex_message = FlexSendMessage(alt_text='Choose a plan', contents=flex_message_reply,quick_reply=quick_reply)
            return flex_message

def create_status_flex_message(plan, remaining_messages, next_update_date, user_language, quick_reply):
    if user_language == 'Portuguese':
        text_title = "Detalhes do plano"
        text_plan = "Plano:"
        text_Remaining_Messages = "Mensagens Restantes:"
        text_next_upadate_date = "Próxima atualização:"
    elif user_language == 'Spanish':
        text_title = "detalles del plan"
        text_plan = "Plan:"
        text_Remaining_Messages = "Mensajes restantes:"
        text_next_upadate_date = "Próxima actualización:"
    elif user_language == 'Tagalog':
        text_title = "mga detalye ng plano"
        text_plan = "Plano:"
        text_Remaining_Messages = "Mga Natitirang Mensahe:"
        text_next_upadate_date = "Susunod na update:"
    elif user_language == 'Vietnamese':
        text_title = "kế hoạch chi tiết"
        text_plan = "kế hoạch:"
        text_Remaining_Messages = "Tin nhắn còn lại:"
        text_next_upadate_date = "Cập nhật tiếp theo:"
    elif user_language == 'Japanese':
        text_title = "Plan Details"
        text_plan = "Plan:"
        text_Remaining_Messages = "Remaining Messages:"
        text_next_upadate_date = "Next Update Date:"
    else:
        text_title = "Plan Details"
        text_plan = "Plan:"
        text_Remaining_Messages = "Remaining Messages:"
        text_next_upadate_date = "Next Update Date:"

    flex_message_reply = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": text_title,
                    "weight": "bold",
                    "size": "xl",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": text_plan,
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{plan} plan",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": text_Remaining_Messages,
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{remaining_messages}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": text_next_upadate_date,
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{next_update_date}",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                    ]
                }
            ]
        }
    }
    flex_message = FlexSendMessage(alt_text='Your Status', contents=flex_message_reply,quick_reply=quick_reply)
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
            QuickReplyButton(action=MessageAction(label="katayuan", text="Sabihin mo sa akin ang status")),
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
    line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
    profile = line_bot_api.get_profile(line_user_id)
    # Get user's language
    user_language = language_codes.language_code_to_name[profile.language]

    # Check if the user exists in DynamoDB
    user_exists = db_accessor.check_line_user_id_exists(line_user_id)

    # Create quick reply buttons
    quick_reply_buttons = create_quick_reply_buttons(user_language)
    quick_reply = QuickReply(items=quick_reply_buttons) 


    # If the user doesn't exist in DynamoDB, insert their data
    if user_exists == "No":
        db_accessor.insert_data(line_user_id, user_language)
        if user_language == 'Portuguese':
            intro_youtube_url   = "https://youtu.be/3FszqkOB-2A"
            upgrade_youtube_url = "https://youtu.be/H4mDq9cNlgg"
            cancel_youtube_url  = "https://youtu.be/y80DEMI_tf8"
            portalsite          = 'https://pictolang-help.freshdesk.com/pt-BR/support/home'
            queryformurl        = 'https://pictolang-help.freshdesk.com/pt-BR/support/tickets/new'
            query_youtube_url   = "https://youtu.be/Zb_UAG20gBU"
            welcome_message = f'''Obrigado por se registrar como amigo no PicToLang. Estamos aqui para responder às suas dúvidas diariamente. Além disso, ao enviar fotos de documentos escritos em outros idiomas, nós faremos a tradução e forneceremos um resumo de alto nível.

Preparamos vídeos no YouTube e um site para ajudá-lo a entender melhor o nosso serviço. Sinta-se à vontade para usar o YouTube e nosso site conforme necessário.

Para uma introdução ao PicToLang do serviço, assista a este vídeo no YouTube:
{intro_youtube_url}

Para aprender a atualizar seu plano, assista a este vídeo no YouTube:
{upgrade_youtube_url}

Para aprender a cancelar seu plano, assista a este vídeo no YouTube:
{cancel_youtube_url}

Visite também nosso site para mais informações:👇
{portalsite}

Caso tenha alguma dúvida, você pode entrar em contato através do link abaixo. 👇
{queryformurl}
O operador responderá. E se não souber como entrar em contato conosco, assista a este vídeo no YouTube:👇
{query_youtube_url}

No momento você é um usuário gratuito (free) e pode enviar 7 mensagens por mês. Se você quiser usar mais do que isso, renove seu plano na guia "Atualizar".
'''
        elif user_language == 'Spanish':
            intro_website_url    = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000076969-pictolang-un-asistente-virtual-revolucionario-que-trasciende-las-barreras-del-idioma"
            upgrade_website_url  = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000079074-c%C3%B3mo-adquirir-nuestros-planes-en-chatbot-pictolang-"
            cancel_website_url   = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000079261-c%C3%B3mo-cancelar-tu-suscripci%C3%B3n-en-chatbot-pictolang-"
            queryformurl         = "https://pictolang-help.freshdesk.com/es-LA/support/tickets/new"
            portalsite           = "https://pictolang-help.freshdesk.com/es-LA/support/home"
            query_website_url    = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000079236-c%C3%B3mo-contactarnos-en-chatbot-pictolang-"
            welcome_message = f'''Gracias por registrarte como amigo en PicToLang. Estamos aquí para responder a tus preguntas todos los días. Además, al enviar fotos de documentos escritos en otros idiomas, haremos la traducción y te proporcionaremos un resumen de alto nivel.

Hemos preparado un sitio web para ayudarte a entender mejor nuestro servicio. No dudes en utilizar nuestro sitio web según sea necesario.

Para una introducción a PicToLang y una demostración del servicio, visita este artículo en nuestro sitio web:
{intro_website_url}

Para aprender a actualizar tu plan, visita este artículo en nuestro sitio web:
{upgrade_website_url}

Para aprender a cancelar tu plan, visita este artículo en nuestro sitio web:
{cancel_website_url}

También puedes visitar nuestro sitio web para más información:👇
{portalsite}

Si tienes alguna pregunta, puedes ponerte en contacto a través del siguiente enlace. 👇
{queryformurl}
El operador responderá. Y si no sabes cómo ponerte en contacto con nosotros, lee este artículo en nuestro sitio web:👇
{query_website_url}

Actualmente eres un usuario gratuito y puedes enviar 7 mensajes al mes. Si deseas usar más que eso, renueva tu plan en la pestaña "Actualizar".
'''
        elif user_language == 'Tagalog':
            intro_website_url    = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000076969-pictolang-isang-makabagong-virtual-na-assistant-na-lumalagpas-sa-mga-hadlang-ng-wika"
            upgrade_website_url  = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000079074-paano-bumili-ng-aming-mga-plano-sa-chatbot-pictolang-"
            cancel_website_url   = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000079261-paano-kanselahin-ang-iyong-subscription-sa-chatbot-pictolang-"
            queryformurl         = "https://pictolang-help.freshdesk.com/fil/support/tickets/new"
            portalsite           = "https://pictolang-help.freshdesk.com/fil/support/home"
            query_website_url    = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000079236-paano-makipag-ugnayan-sa-amin-sa-chatbot-pictolang-"
            welcome_message = f'''Salamat sa iyong pagpaparehistro bilang kaibigan sa PicToLang. Nandito kami upang sagutin ang iyong mga katanungan araw-araw. Dagdag pa, sa pagsumite ng mga larawan ng mga dokumentong nakasulat sa iba't ibang wika, kami ay magtatranslate at magbibigay sa iyo ng isang komprehensibong buod.

Naghanda kami ng website upang matulungan kang mas maunawaan ang aming serbisyo. Huwag mag-atubiling gamitin ang aming website kung kinakailangan.

Para sa isang introduksyon sa PicToLang at isang demonstrasyon ng serbisyo, bisitahin ang artikulong ito sa aming website:
{intro_website_url}

Para malaman kung paano i-upgrade ang iyong plano, bisitahin ang artikulong ito sa aming website:
{upgrade_website_url}

Para malaman kung paano kanselahin ang iyong plano, bisitahin ang artikulong ito sa aming website:
{cancel_website_url}

Maaari mo ring bisitahin ang aming website para sa karagdagang impormasyon:👇
{portalsite}

Kung mayroon kang anumang katanungan, maaari kang makipag-ugnay sa pamamagitan ng sumusunod na link. 👇
{queryformurl}
Ang operator ay magrerespond. At kung hindi mo alam kung paano makipag-ugnay sa amin, basahin ang artikulong ito sa aming website:👇
{query_website_url}

Sa kasalukuyan, ikaw ay isang libreng gumagamit at maaaring magpadala ng 7 mga mensahe kada buwan. Kung nais mong gumamit ng higit pa sa iyon, i-renew ang iyong plano sa tab na "Update".
'''

        elif user_language == 'Vietnamese':
            intro_website_url    = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000076969-pictolang-tr%E1%BB%A3-l%C3%BD-%E1%BA%A3o-c%C3%A1ch-m%E1%BA%A1ng-v%C6%B0%E1%BB%A3t-qua-r%C3%A0o-c%E1%BA%A3n-ng%C3%B4n-ng%E1%BB%AF"
            upgrade_website_url  = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000079074-c%C3%A1ch-%C4%91%E1%BB%83-mua-c%C3%A1c-g%C3%B3i-c%E1%BB%A7a-ch%C3%BAng-t%C3%B4i-tr%C3%AAn-chatbot-pictolang-"
            cancel_website_url   = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000079261-c%C3%A1ch-h%E1%BB%A7y-%C4%91%C4%83ng-k%C3%BD-tr%C3%AAn-chatbot-pictolang-"
            queryformurl         = "https://pictolang-help.freshdesk.com/vi/support/tickets/new"
            portalsite           = "https://pictolang-help.freshdesk.com/vi/support/home"
            query_website_url    = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000079236-c%C3%A1ch-li%C3%AAn-h%E1%BB%87-v%E1%BB%9Bi-ch%C3%BAng-t%C3%B4i-tr%C3%AAn-chatbot-pictolang-"
            welcome_message = f'''Cảm ơn bạn đã đăng ký làm bạn với PicToLang. Chúng tôi ở đây để trả lời câu hỏi của bạn mỗi ngày. Ngoài ra, bằng cách gửi ảnh của các tài liệu viết bằng ngôn ngữ khác, chúng tôi sẽ thực hiện việc dịch và cung cấp cho bạn một bản tóm tắt cấp cao.

Chúng tôi đã chuẩn bị một trang web để giúp bạn hiểu rõ hơn về dịch vụ của chúng tôi. Hãy sử dụng trang web của chúng tôi khi cần.

Để tìm hiểu về PicToLang và dịch vụ, hãy truy cập bài viết này trên trang web của chúng tôi:
{intro_website_url}

Để tìm hiểu cách nâng cấp kế hoạch của bạn, hãy truy cập bài viết này trên trang web của chúng tôi:
{upgrade_website_url}

Để tìm hiểu cách hủy kế hoạch của bạn, hãy truy cập bài viết này trên trang web của chúng tôi:
{cancel_website_url}

Bạn cũng có thể truy cập trang web của chúng tôi để biết thêm thông tin:👇
{portalsite}

Nếu bạn có bất kỳ câu hỏi nào, bạn có thể liên hệ qua liên kết sau. 👇
{queryformurl}
Người điều hành sẽ trả lời. Và nếu bạn không biết cách liên hệ với chúng tôi, hãy đọc bài viết này trên trang web của chúng tôi:👇
{query_website_url}

Hiện tại, bạn là người dùng miễn phí và có thể gửi 7 tin nhắn mỗi tháng. Nếu bạn muốn sử dụng nhiều hơn, hãy gia hạn kế hoạch của bạn trong tab "Cập nhật".
'''

        elif user_language == 'Japanese':
            intro_website_url    = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000076969-pictolang-a-revolutionary-virtual-assistant-that-transcends-language-barriers"
            upgrade_website_url  = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079074-how-to-acquire-our-plans-in-chatbot-pictolang-"
            cancel_website_url   = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079261-how-to-cancel-your-subscription-in-chatbot-pictolang-"
            queryformurl         = "https://pictolang-help.freshdesk.com/ja-JP/support/tickets/new"
            portalsite           = "https://pictolang-help.freshdesk.com/en/support/home"
            query_website_url    = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079236-how-to-contact-us-in-chatbot-pictolang-"
            welcome_message = f'''PicToLangを友達登録いただき、ありがとうございます。私たちの日常的に生じる疑問にお答えしています。さらに、他の言語で書かれた文書の写真を投稿することで、高いレベルで翻訳や要約を提供します。

私たちのサービスをよりよく理解頂くためにWebサイトをご用意しました。必要に応じてご活用ください。

PicToLangの紹介は、以下のこの記事をご覧ください：
{intro_website_url}

プランのアップグレード方法については、以下の記事をご覧ください：
{upgrade_website_url}

プランのキャンセル方法については、以下の記事をご覧ください：
{cancel_website_url}

また、ポートタルサイトは以下になります：👇
{portalsite}

お問合せは、以下のリンクからお願いいたします。👇
{queryformurl}
オペレーターが回答します。お問合せ方法が分からない場合は、以下の記事をご覧ください：👇
{query_website_url}

現在、あなたは無料ユーザー(free)であり、月に7件のメッセージを送信できます。それ以上を使用したい場合は、"更新"タブからプランを更新してください。
'''

        else:
            intro_website_url    = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000076969-pictolang-a-revolutionary-virtual-assistant-that-transcends-language-barriers"
            upgrade_website_url  = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079074-how-to-acquire-our-plans-in-chatbot-pictolang-"
            cancel_website_url   = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079261-how-to-cancel-your-subscription-in-chatbot-pictolang-"
            queryformurl         = "https://pictolang-help.freshdesk.com/en/support/tickets/new"
            portalsite           = "https://pictolang-help.freshdesk.com/en/support/home"
            query_website_url    = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079236-how-to-contact-us-in-chatbot-pictolang-"
            welcome_message = f'''Thank you for registering as a friend in PicToLang. We are here to answer your questions every day. Additionally, by submitting photos of documents written in other languages, we will do the translation and provide you with a high-level summary.

We have prepared a website to help you better understand our service. Feel free to utilize our website as needed.

For an introduction to PicToLang of the service, visit this article on our website:
{intro_website_url}

To learn how to upgrade your plan, visit this article on our website:
{upgrade_website_url}

To learn how to cancel your plan, visit this article on our website:
{cancel_website_url}

You can also visit our website for more information:👇
{portalsite}

If you have any questions, you can get in touch through the following link. 👇
{queryformurl}
The operator will respond. And if you don't know how to contact us, read this article on our website:👇
{query_website_url}

Currently, you are a free user and can send 7 messages per month. If you wish to use more than that, renew your plan in the "Update" tab.
'''


    else:
        user_data = db_accessor.get_line_user_data(line_user_id)
        plan = user_data['plan']
        message_count = user_data['message_count']
        if user_language == 'Portuguese':
            welcome_message = f"Obrigado por se juntar a nós novamente.\nAtualmente, você é um usuário do {plan} e tem {message_count} mensagens restantes este mês.\nObrigado por seu apoio contínuo."
        elif user_language == 'Spanish':
            welcome_message = f"Gracias por volver a unirte a nosotros.\nActualmente eres usuario de {plan} y te quedan {message_count} mensajes este mes.\nGracias por tu continuo apoyo."
        elif user_language == 'English':
            welcome_message = f"Thank you for joining us again.\nYou are currently a {plan} user and have {message_count} messages left this month.\nThank you for your continued support."
        elif user_language == 'Tagalog':
            welcome_message = f"Salamat sa muling pagsali sa amin.\nKasalukuyan kang user ng {plan} at may natitirang {message_count} na mensahe ngayong buwan.\nSalamat sa iyong patuloy na suporta."
        elif user_language == 'Vietnamese':
            welcome_message = f"Cảm ơn bạn đã tham gia cùng chúng tôi một lần nữa.\nBạn hiện là người dùng {plan} và còn {message_count} tin nhắn trong tháng này.\nCảm ơn bạn đã tiếp tục hỗ trợ."
        elif user_language == 'Japanese':
            welcome_message = f"再び友達登録いただきありがとうございます。\nあなたは現在 {plan} ユーザーで、今月は {message_count} 回のメッセージを送信可能です。\n今後ともよろしくお願いいたします。"
        else:
            welcome_message = f"Thank you for joining us again.\nYou are currently a {plan} user and have {message_count} messages left this month.\nThank you for your continued support."

    # Reply the welcome message using the LineBotApi instance
    line_api.reply_message_for_line(reply_token, welcome_message, quick_reply)  # Consider removing QuickReply or using a different function for sending the message

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

    if prompt_text == "Quiero actualizar mi aplicación." or prompt_text == "Eu quero atualizar meu aplicativo" or prompt_text == "アップグレードしたいです" or prompt_text == "Tôi muốn cập nhật ứng dụng"or prompt_text == "Gusto kong i-update ang aking app"or prompt_text == "I want to upgrade my app":
        plan = db_accessor.get_user_plan(line_user_id)
        print("plan:",plan)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)
        if plan == "free":
            flex_message = send_flex_message(plan, line_user_id, quick_reply,user_language)
        else:
            flex_message = send_flex_message_upgrade(plan,quick_reply,user_language)

        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

        from linebot.exceptions import LineBotApiError
        try:
            if user_language == 'Portuguese':
                upgrade_youtube_url = "https://youtu.be/H4mDq9cNlgg"
                upgrade_article_url = "https://pictolang-help.freshdesk.com/pt-BR/support/solutions/articles/150000079074-como-adquirir-nossos-planos-no-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Seu plano é {plan} plan.
                                                    Por favor, selecione o plano que deseja fazer atualizar ou rebaixar no botão abaixo.
                                                    Para aprender a atualizar seu plano, assista a este vídeo no YouTube:👇\n{upgrade_youtube_url}
                                                    Além disso, também preparamos um artigo que pode ser útil para você. Para acessar o artigo, visite este link:👇\n{upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Spanish':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000079074-c%C3%B3mo-adquirir-nuestros-planes-en-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Tu plan es {plan} plan.
                                                    Por favor, selecciona el plan que deseas actualizar o degradar en el botón de abajo.
                                                    Además, hemos preparado un artículo que podría ser útil para ti. Para acceder al artículo, visita este enlace:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000079074-paano-bumili-ng-aming-mga-plano-sa-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Ang iyong plano ay {plan} plan.
                                                    Mangyaring piliin ang plano na nais mong i-upgrade o i-downgrade gamit ang button sa ibaba.
                                                    Bukod dito, nag-ihanda kami ng isang artikulo na maaaring makatulong sa iyo. Para ma-access ang artikulo, bisitahin ang link na ito:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000079074-c%C3%A1ch-%C4%91%E1%BB%83-mua-c%C3%A1c-g%C3%B3i-c%E1%BB%A7a-ch%C3%BAng-t%C3%B4i-tr%C3%AAn-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Kế hoạch của bạn là {plan} plan.
                                                    Vui lòng chọn kế hoạch bạn muốn nâng cấp hoặc hạ cấp bằng cách sử dụng nút dưới đây.
                                                    Ngoài ra, chúng tôi đã chuẩn bị một bài viết có thể hữu ích cho bạn. Để truy cập bài viết, hãy truy cập liên kết này:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Japanese':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079074-how-to-acquire-our-plans-in-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    あなたのプランは {plan} planです。
                                                    下のボタンからアップグレードまたはダウングレードしたいプランを選択してください。
                                                    また、アップグレード方法に関する記事は以下になります:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            else:
                upgrade_article_url = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079074-how-to-acquire-our-plans-in-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Your plan is {plan} plan.
                                                    Please select the plan you wish to upgrade or downgrade using the button below.
                                                    In addition, we've prepared an article that might be helpful to you. To access the article, visit this link:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            line_bot_api.reply_message(reply_token, [text_message, flex_message])
            
        except LineBotApiError as e:
            print("Error:", e)

    elif prompt_text == "Contato conosco" or prompt_text == "contacto" or prompt_text == "お問い合せ" or prompt_text == "Liên hệ với chúng tôi" or prompt_text == "Makipag-ugnay sa amin" or prompt_text == "Contact us":
         # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        from linebot.exceptions import LineBotApiError
        try:
            if user_language == 'Portuguese':
                queryformurl = "https://pictolang-help.freshdesk.com/pt-BR/support/tickets/new"
                query_youtube_url = "https://youtu.be/Zb_UAG20gBU"
                query_article_url = "https://pictolang-help.freshdesk.com/pt-BR/support/solutions/articles/150000079236-como-entrar-em-contato-conosco-no-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Por favor, preencha as informações necessárias no link (Enviar um ticket) abaixo e envie-o.👇\n{queryformurl}
                                                        Depois de clicar no link(Enviar um ticket), se você inserir o seguinte valor em "ID do usuário", poderei pesquisar seu histórico e status de mensagens anteriores. Você obterá melhores respostas. Se você não se importa, insira os seguintes valores e envie.

                                                        Seu ID do usuário👇\n{line_user_id}

                                                        Além disso, preparamos um vídeo no YouTube e um artigo explicando como entrar em contato conosco. Para assistir ao vídeo, visite este link:👇\n{query_youtube_url}                                                        Para ler o artigo sobre como entrar em contato conosco, visite este link:👇\n{query_article_url}
                                                        """, quick_reply=quick_reply)
            elif user_language == 'Spanish':
                queryformurl = "https://pictolang-help.freshdesk.com/es-LA/support/tickets/new"
                query_article_url = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000079236-c%C3%B3mo-contactarnos-en-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Por favor, completa la información necesaria en el enlace (Enviar un ticket) a continuación y envíalo.👇\n{queryformurl}
                                                        Después de hacer clic en el enlace (Enviar un ticket), si introduces el siguiente valor en "ID de usuario", podré buscar tu historial y estado de mensajes anteriores. Obtendrás mejores respuestas. Si no te importa, introduce los siguientes valores y envía.

                                                        Tu ID de usuario👇\n{line_user_id}

                                                        Además, hemos preparado un artículo que explica cómo ponerse en contacto con nosotros. Para leer el artículo sobre cómo ponerse en contacto con nosotros, visita este enlace:👇\n{query_article_url}
                                                        """, quick_reply=quick_reply)

            elif user_language == 'Tagalog':
                queryformurl = "https://pictolang-help.freshdesk.com/fil/support/tickets/new"
                query_article_url = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000079236-paano-makipag-ugnayan-sa-amin-sa-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Pakipunan ang kinakailangang impormasyon sa link (Magsumite ng isang ticket) sa ibaba at ipadala ito.👇\n{queryformurl}
                                                        Pagkatapos mag-click sa link (Magsumite ng isang ticket), kung ipapasok mo ang sumusunod na halaga sa "User ID", maaari kong hanapin ang iyong kasaysayan ng nakaraang mensahe at estado. Makakakuha ka ng mas mahusay na mga tugon. Kung hindi ka nag-aalala, pakipasok ang mga sumusunod na halaga at ipadala.

                                                        Ang iyong User ID👇\n{line_user_id}

                                                        Bukod dito, nakahanda kami ng isang artikulo na nagpapaliwanag kung paano makipag-ugnay sa amin.Para mabasa ang artikulo tungkol sa kung paano makipag-ugnay sa amin, bisitahin ang link na ito:👇\n{query_article_url}
                                                        """, quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                queryformurl = "https://pictolang-help.freshdesk.com/vi/support/tickets/new"
                query_article_url = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000079236-c%C3%A1ch-li%C3%AAn-h%E1%BB%87-v%E1%BB%9Bi-ch%C3%BAng-t%C3%B4i-tr%C3%AAn-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Vui lòng điền thông tin cần thiết vào liên kết (Gửi một vé) dưới đây và gửi đi.👇\n{queryformurl}
                                                        Sau khi nhấp vào liên kết (Gửi một vé), nếu bạn nhập giá trị sau vào "User ID", tôi có thể tìm kiếm lịch sử tin nhắn trước đó và trạng thái của bạn. Bạn sẽ nhận được các phản hồi tốt hơn. Nếu bạn không phiền, vui lòng nhập các giá trị sau và gửi đi.

                                                        User ID của bạn👇\n{line_user_id}

                                                        Ngoài ra, chúng tôi đã chuẩn bị một bài viết giải thích cách liên lạc với chúng tôi.Để đọc bài viết về cách liên lạc với chúng tôi, hãy truy cập liên kết này:👇\n{query_article_url}
                                                        """, quick_reply=quick_reply)
            elif user_language == 'Japanese':
                queryformurl = "https://pictolang-help.freshdesk.com/en/support/tickets/new"
                query_article_url = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079236-how-to-contact-us-in-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""必要な情報を以下のリンク（チケットを提出）に入力して送信してください。👇\n{queryformurl}
                                                        リンク（チケットを提出）をクリックした後、「User ID」に次の値を入力すると、ユーザーの過去のメッセージの履歴とステータスを検索することができます。より良い回答を得ることができます。もしよろしければ、以下の値を入力して送信してください。

                                                        あなたのUser ID👇\n{line_user_id}

                                                        また、問い合わせ方法を説明した記事を用意しています。 記事は以下になります。ご参照ください：👇\n{query_article_url}
                                                        """, quick_reply=quick_reply)
            else:
                queryformurl = "https://pictolang-help.freshdesk.com/en/support/tickets/new"
                query_article_url = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079236-how-to-contact-us-in-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Please fill in the necessary information in the link (Submit a ticket) below and send it.👇\n{queryformurl}
                                                        After clicking the link (Submit a ticket), if you enter the following value in "User ID", I can search your previous message history and status. You will get better responses. If you don't mind, please enter the following values and send.

                                                        Your User ID👇\n{line_user_id}

                                                        In addition, we've prepared an article explaining how to get in touch with us.To read the article on how to contact us, visit this link:👇\n{query_article_url}
                                                        """, quick_reply=quick_reply)



            line_bot_api.reply_message(reply_token, text_message)
            # line_bot_api.reply_message(reply_token, [text_message, flex_message])
        except LineBotApiError as e:
            print("Error:", e)

    elif prompt_text == "Quero cancelar o aplicativo" or prompt_text == "Quiero cancelar la aplicación" or prompt_text == "解約したいです" or prompt_text == "Tôi muốn hủy ứng dụng" or prompt_text == "Gusto kong kanselahin ang app" or prompt_text == "I want to cancel the app":
        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)
        from linebot.exceptions import LineBotApiError
        try:
            if user_language == 'Portuguese':
                actions = [
                        MessageAction(label="Sim", text="sim vou cancelar"),
                        MessageAction(label="Não", text="Não, continuarei com meu contrato atual"),
                      ]
                # Create a ConfirmTemplate
                confirm_template = ConfirmTemplate(text="Você tem certeza que deseja cancelar?", actions=actions)
            elif user_language == 'Spanish':
                actions = [
                        MessageAction(label="Sí", text="si voy a cancelar"),
                        MessageAction(label="No", text="No, continuaré con mi contrato actual."),
                      ]
                # Create a ConfirmTemplate
                confirm_template = ConfirmTemplate(text="¿Estas seguro que quieres cancelar?", actions=actions)
            elif user_language == 'Tagalog':
                actions = [
                        MessageAction(label="Oo", text="oo kakanselahin ko"),
                        MessageAction(label="Hindi", text="Hindi, ipagpapatuloy ko ang aking kasalukuyang kontrata"),
                      ]
                # Create a ConfirmTemplate
                confirm_template = ConfirmTemplate(text="Sigurado ka bang gusto mong kanselahin?", actions=actions)
            elif user_language == 'Vietnamese':
                actions = [
                        MessageAction(label="Đúng", text="vâng tôi sẽ hủy"),
                        MessageAction(label="Không", text="Không, tôi sẽ tiếp tục hợp đồng hiện tại của mình"),
                      ]
                # Create a ConfirmTemplate
                confirm_template = ConfirmTemplate(text="Bạn có chắc là muốn hủy bỏ?", actions=actions)
            elif user_language == 'Japanese':
                actions = [
                        MessageAction(label="はい", text="はい、私は本当に解約します。"),
                        MessageAction(label="いいえ", text="いいえ、引き続き今の契約を続けます。"),
                      ]
                # Create a ConfirmTemplate
                confirm_template = ConfirmTemplate(text="本当に解約しますか？", actions=actions)
            else:
                actions = [
                        MessageAction(label="Yes", text="yes I will cancel"),
                        MessageAction(label="No", text="No, I will continue my current contract"),
                      ]
                # Create a ConfirmTemplate
                confirm_template = ConfirmTemplate(text="Are you sure you want to cancel?", actions=actions)

            # Create a TemplateSendMessage with the ConfirmTemplate
            message = TemplateSendMessage(alt_text="this is a confirm template", template=confirm_template)

            line_bot_api.reply_message(reply_token, message)
        except LineBotApiError as e:
            print("Error:", e)

    elif prompt_text == "はい、私は本当に解約します。" or prompt_text == "sim vou cancelar" or prompt_text == "si voy a cancelar" or prompt_text == "oo kakanselahin ko" or prompt_text == "vâng tôi sẽ hủy" or prompt_text == "yes I will cancel":

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

        else:
            print("No active subscription found for this customer.")

            if user_language == 'Portuguese':
                text_message = TextSendMessage(text="Não foi possível encontrar seu plano. Entre em contato conosco a partir do URL abaixo.\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new", quick_reply=quick_reply)
            elif user_language == 'Spanish':
                text_message = TextSendMessage(text="No se pudo encontrar su plan. Póngase en contacto con nosotros desde la siguiente URL.\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new", quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                text_message = TextSendMessage(text="Hindi mahanap ang iyong plano. Mangyaring makipag-ugnay sa amin mula sa URL sa ibaba.\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new", quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                text_message = TextSendMessage(text="Không thể tìm thấy kế hoạch của bạn. Vui lòng liên hệ với chúng tôi từ URL bên dưới.\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new", quick_reply=quick_reply)
            elif user_language == 'Japanese':
                text_message = TextSendMessage(text="あなたのプランを見つけることができませんでした。以下URLよりお問合せください。\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new", quick_reply=quick_reply)
            else:
                text_message = TextSendMessage(text="Could not find your plan. Please contact us from the URL below.\nhttps://pictolang-help.freshdesk.com/pt-BR/support/tickets/new", quick_reply=quick_reply)

            # Push the message to the user
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            from linebot.exceptions import LineBotApiError
            try:
                line_bot_api.reply_message(reply_token, text_message)
            except LineBotApiError as e:
                print("Error:", e)
    
    elif prompt_text == "Quero assinar o basic plan" or prompt_text == "Quero assinar o standard plan" or prompt_text == "Quero assinar o premium plan" or prompt_text == "Quiero suscribirme al basic plan" or prompt_text == "Quiero suscribirme al standard plan" or prompt_text == "Quiero suscribirme al premium plan" or prompt_text == "Gusto kong mag-subscribe sa basic plan" or prompt_text == "Gusto kong mag-subscribe sa standard plan" or prompt_text == "Gusto kong mag-subscribe sa premium plan" or prompt_text == "Tôi muốn đăng ký basic plan" or prompt_text == "Tôi muốn đăng ký standard plan" or prompt_text == "Tôi muốn đăng ký premium plan" or prompt_text == "basic planを契約したいです。" or prompt_text == "standard planを契約したいです。" or prompt_text == "premium planを契約したいです。" or prompt_text == "I want to subscribe to the basic plan" or prompt_text == "I want to subscribe to the standard plan" or prompt_text == "I want to subscribe to the premium plan":
        if prompt_text == "Quero assinar o basic plan"  or prompt_text == "Quero assinar o standard plan" or prompt_text == "Quero assinar o premium plan":
            if prompt_text == "Quero assinar o basic plan":
                plan = "basic"
                send_text = "Você pode enviar 100 mensagens por 80 ienes mensais."
            elif prompt_text == "Quero assinar o standard plan":
                plan = "standard"
                send_text = "Você pode enviar 300 mensagens por 230 ienes mensais."
            elif prompt_text == "Quero assinar o premium plan":
                plan = "premium"
                send_text = "Você pode enviar mensagens ilimitadas por 750 ienes mensais."
            label_yes = "Sim"
            label_no = "Não"
            text_yes = f"sim. Eu assino o {plan}."
            text_no = "Não, continuarei com meu contrato atual"
            confirm_template_text = f'Em {plan} plan, {send_text} Se desejar finalizar o contrato, clique em "Sim" abaixo'

        elif prompt_text == "Quiero suscribirme al basic plan" or prompt_text == "Quiero suscribirme al standard plan" or prompt_text == "Quiero suscribirme al premium plan":
            if prompt_text == "Quiero suscribirme al basic plan":
                plan = "basic"
                send_text = "Puede enviar 100 mensajes por mes por 80 yen por mes."
            elif prompt_text == "Quiero suscribirme al standard plan":
                plan = "standard"
                send_text = "Puede enviar 300 mensajes por mes por 230 yen por mes."
            elif prompt_text == "Quiero suscribirme al premium plan":
                plan = "premium"
                send_text = "Puedes enviar mensajes ilimitados por 750 yen al mes."
            label_yes = "Sí"
            label_no = "No"
            text_yes = f"Sí. Me suscribo al {plan}."
            text_no = "No, continuaré con mi contrato actual."
            confirm_template_text = f'En {plan} plan, {send_text} Si desea finalizar el contrato, haga clic en "Sí" a continuación'

        elif prompt_text == "Gusto kong mag-subscribe sa basic plan" or prompt_text == "Gusto kong mag-subscribe sa standard plan" or prompt_text == "Gusto kong mag-subscribe sa premium plan":
            if prompt_text == "Gusto kong mag-subscribe sa basic plan":
                plan = "basic"
                send_text = "Maaari kang magpadala ng 100 mensahe bawat buwan sa halagang 80 yen bawat buwan."
            elif prompt_text == "Gusto kong mag-subscribe sa standard plan":
                plan = "standard"
                send_text = "Maaari kang magpadala ng 300 mensahe bawat buwan sa halagang 230 yen bawat buwan."
            elif prompt_text == "Gusto kong mag-subscribe sa premium plan":
                plan = "premium"
                send_text = "Maaari kang magpadala ng walang limitasyong mga mensahe sa halagang 750yen bawat buwan."
            label_yes = "Oo"
            label_no = "Hindi"
            text_yes = f"Oo. Nag-subscribe ako sa {plan}."
            text_no = "Hindi, ipagpapatuloy ko ang aking kasalukuyang kontrata"
            confirm_template_text = f'Sa {plan} plan, {send_text} Kung gusto mong tapusin ang kontrata, i-click ang "Oo" sa ibaba'
        
        elif prompt_text == "Tôi muốn đăng ký basic plan" or prompt_text == "Tôi muốn đăng ký standard plan" or prompt_text == "Tôi muốn đăng ký premium plan":
            if prompt_text == "Tôi muốn đăng ký basic plan":
                plan = "basic"
                send_text = "Bạn có thể gửi 100 tin nhắn mỗi tháng với 80 yên mỗi tháng."
            elif prompt_text == "Tôi muốn đăng ký standard plan":
                plan = "standard"
                send_text = "Bạn có thể gửi 300 tin nhắn mỗi tháng với 230 yên mỗi tháng."
            elif prompt_text == "Tôi muốn đăng ký premium plan":
                plan = "premium"
                send_text = "Bạn có thể gửi tin nhắn không giới hạn với 750 yên mỗi tháng."
            label_yes = "Đúng"
            label_no = "Không"
            text_yes = f"Đúng. Tôi đăng ký {plan}."
            text_no = "Không, tôi sẽ tiếp tục hợp đồng hiện tại của mình"
            confirm_template_text = f'Trong gói {plan}, {send_text} Nếu bạn muốn kết thúc hợp đồng, hãy nhấp vào "Có" bên dưới'
        
        elif prompt_text == "basic planを契約したいです。" or prompt_text == "standard planを契約したいです。" or prompt_text == "premium planを契約したいです。":
            if prompt_text == "basic planを契約したいです。":
                plan = "basic"
                send_text = "月額80円で月100通までメッセージを送信可能です。"
            elif prompt_text == "standard planを契約したいです。":
                plan = "standard"
                send_text = "月額230円で月300通までメッセージを送信可能です。"
            elif prompt_text == "premium planを契約したいです。":
                plan = "premium"
                send_text = "月額750円でメッセージを無制限に送信可能です。"
            label_yes = "はい"
            label_no = "いいえ"
            text_yes = f"はい。私は{plan}を契約します。"
            text_no = "いいえ、引き続き今の契約を続けます。"
            confirm_template_text = f'{plan} planでは、{send_text} 契約を完了させるには、下の [はい] をクリックしてください'
        
        elif prompt_text == "I want to subscribe to the basic plan" or prompt_text == "I want to subscribe to the standard plan" or prompt_text == "I want to subscribe to the premium plan":
            if prompt_text == "I want to subscribe to the basic plan":
                plan = "basic"
                send_text = "You can send 100 messages per month for 80 yen per month."
            elif prompt_text == "I want to subscribe to the standard plan":
                plan = "standard"
                send_text = "You can send 300 messages per month for 230 yen per month."
            elif prompt_text == "I want to subscribe to the premium plan":
                plan = "premium"
                send_text = "You can send unlimited messages for 750 yen per month."
            label_yes = "Yes"
            label_no = "No"
            text_yes = f"Yes. I subscribe to the {plan}."
            text_no = "No, I will continue my current contract"
            confirm_template_text = f'In {plan} plan, {send_text} If you want to end the contract, click "Yes" below'

        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)
        from linebot.exceptions import LineBotApiError
        try:
            actions = [
                        MessageAction(label=label_yes, text=text_yes),
                        MessageAction(label=label_no, text=text_no),
                      ]
            # Create a ConfirmTemplate
            confirm_template = ConfirmTemplate(text=confirm_template_text, actions=actions)

            # Create a TemplateSendMessage with the ConfirmTemplate
            message = TemplateSendMessage(alt_text="this is a confirm template", template=confirm_template)

            line_bot_api.reply_message(reply_token, message)

        except LineBotApiError as e:
            print("Error:", e)

    elif prompt_text == "sim. Eu assino o basic." or prompt_text == "sim. Eu assino o standard." or prompt_text == "sim. Eu assino o premium." or prompt_text == "Sí. Me suscribo al basic." or prompt_text == "Sí. Me suscribo al standard." or prompt_text == "Sí. Me suscribo al premium." or prompt_text == "Oo. Nag-subscribe ako sa basic." or prompt_text == "Oo. Nag-subscribe ako sa standard." or prompt_text == "Oo. Nag-subscribe ako sa premium." or prompt_text == "Đúng. Tôi đăng ký basic." or prompt_text == "Đúng. Tôi đăng ký standard." or prompt_text == "Đúng. Tôi đăng ký premium." or prompt_text == "はい。私はbasicを契約します。" or prompt_text == "はい。私はstandardを契約します。"or prompt_text == "はい。私はpremiumを契約します。" or prompt_text == "Yes. I subscribe to the basic." or prompt_text == "Yes. I subscribe to the standard." or prompt_text == "Yes. I subscribe to the premium.":

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

        if prompt_text == "はい。私はbasicを契約します。" or prompt_text == "sim. Eu assino o basic." or prompt_text == "Sí. Me suscribo al basic." or prompt_text == "Oo. Nag-subscribe ako sa basic." or prompt_text == "Đúng. Tôi đăng ký basic." or prompt_text == "Yes. I subscribe to the basic.":
            new_plan_id = const.PRICE_ID_BASIC
        elif prompt_text == "はい。私はstandardを契約します。" or prompt_text == "sim. Eu assino o standard." or prompt_text == "Sí. Me suscribo al standard." or prompt_text == "Oo. Nag-subscribe ako sa standard." or prompt_text == "Đúng. Tôi đăng ký standard." or prompt_text == "Yes. I subscribe to the standard.":
            new_plan_id = const.PRICE_ID_STANDARD
        elif prompt_text == "はい。私はpremiumを契約します。" or prompt_text == "sim. Eu assino o premium." or prompt_text == "Sí. Me suscribo al premium." or prompt_text == "Oo. Nag-subscribe ako sa premium." or prompt_text == "Đúng. Tôi đăng ký premium." or prompt_text == "Yes. I subscribe to the premium.":
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
                billing_cycle_anchor="now",
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

        except Exception as e:
            print(f"Error upgrading subscription: {e}")
            return None
        
    elif prompt_text == "Não, continuarei com meu contrato atual" or prompt_text == "No, continuaré con mi contrato actual." or prompt_text == "Không, tôi sẽ tiếp tục hợp đồng hiện tại của mình" or prompt_text == "Không, tôi sẽ tiếp tục hợp đồng hiện tại của mình" or prompt_text == "いいえ、引き続き今の契約を続けます。"or prompt_text == "No, I will continue my current contract":
         # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        from linebot.exceptions import LineBotApiError
        try:

            if user_language == 'Portuguese':
                text_message = TextSendMessage(text=f"Eu entendi. Continue a usar o PicToLang com seu contrato atual.", quick_reply=quick_reply)
            elif user_language == 'Spanish':
                text_message = TextSendMessage(text=f"Continúe usando PicToLang con su contrato actual.", quick_reply=quick_reply)
            elif user_language == 'English':
                text_message = TextSendMessage(text=f"I've got it. Please continue to use PicToLang with your current contract.", quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                text_message = TextSendMessage(text=f"Nakuha ko na. Mangyaring patuloy na gamitin ang PicToLang sa iyong kasalukuyang kontrata.", quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                text_message = TextSendMessage(text=f"Tôi hiểu rồi. Vui lòng tiếp tục sử dụng PicToLang với hợp đồng hiện tại của bạn.", quick_reply=quick_reply)
            elif user_language == 'Japanese':
                text_message = TextSendMessage(text=f"承知しました。引き続き今の契約でPicToLangをご活用ください。", quick_reply=quick_reply)
            else:
                text_message = TextSendMessage(text=f"I've got it. Please continue to use PicToLang with your current contract.", quick_reply=quick_reply)

            line_bot_api.reply_message(reply_token, text_message)
            # line_bot_api.reply_message(reply_token, [text_message, flex_message])
        except LineBotApiError as e:
            print("Error:", e)
    
    elif prompt_text == "Dime el estado." or prompt_text == "今のステータスを教えてください" or prompt_text == "Diga-me o estado." or prompt_text == "Cho tôi biết trạng thái" or prompt_text == "Sabihin mo sa akin ang status" or prompt_text == "Tell me the status.":
        # Push the message to the user
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        plan = db_accessor.get_user_plan(line_user_id)
        print("plan:",plan)
        remaining_messages = db_accessor.get_current_message_count(line_user_id)
        print("remaining_messages:",remaining_messages)

        next_update_date = db_accessor.get_next_update_date(line_user_id)
        print("remaining_messages:",next_update_date)

        flex_message = create_status_flex_message(plan, remaining_messages, next_update_date, user_language, quick_reply)

        from linebot.exceptions import LineBotApiError
        try:
            line_bot_api.reply_message(reply_token, flex_message)
        except LineBotApiError as e:
            print("Error:", e)


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
            # Create quick reply buttons
            quick_reply_buttons = create_quick_reply_buttons(user_language)
            quick_reply = QuickReply(items=quick_reply_buttons)

            plan = db_accessor.get_user_plan(line_user_id)
            print("plan:",plan)
            if plan == "free":
                flex_message = send_flex_message(plan, line_user_id, quick_reply,user_language)
            else:
                flex_message = send_flex_message_upgrade(plan,quick_reply,user_language)

            if user_language == 'Portuguese':
                text_message = TextSendMessage(text=f"Acabou o seu número máximo de mensagens que pode enviar este mês. Seu plano é {plan}. Se você deseja enviar mais mensagens, selecione o plano que deseja atualizar no botão abaixo.", quick_reply=quick_reply)
            elif user_language == 'Spanish':
                text_message = TextSendMessage(text=f"Ha finalizado el número máximo de mensajes que puede enviar este mes. Su plan es {plan}. Si desea enviar más mensajes, seleccione el plan que desea actualizar desde el botón a continuación.", quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                text_message = TextSendMessage(text=f"Ang iyong maximum na bilang ng mga mensahe na maaari mong ipadala sa buwang ito ay natapos na. Ang iyong plano ay {plan}. Kung gusto mong magpadala ng higit pang mga mensahe, piliin ang planong gusto mong i-upgrade mula sa button sa ibaba.", quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                text_message = TextSendMessage(text=f"Số lượng tin nhắn tối đa bạn có thể gửi trong tháng này đã hết. Kế hoạch của bạn là {plan}. Nếu bạn muốn gửi nhiều tin nhắn hơn, hãy chọn gói bạn muốn nâng cấp từ nút bên dưới.", quick_reply=quick_reply)
            elif user_language == 'Japanese':
                text_message = TextSendMessage(text=f"今月送信可能なメッセージ回数が終了しました。あなたのプランは {plan} です。さらにメッセージを送信したい場合は、下のボタンからアップグレードしたいプランを選択してください。", quick_reply=quick_reply)
            else :
                text_message = TextSendMessage(text=f"Your maximum number of messages you can send this month has ended. Your plan is {plan}. If you want to send more messages, select the plan you want to upgrade from the button below.", quick_reply=quick_reply)
            if user_language == 'Portuguese':
                upgrade_youtube_url = "https://youtu.be/H4mDq9cNlgg"
                upgrade_article_url = "https://pictolang-help.freshdesk.com/pt-BR/support/solutions/articles/150000079074-como-adquirir-nossos-planos-no-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""Acabou o seu número máximo de mensagens que pode enviar este mês.
                                                    Seu plano é {plan} plan.
                                                    Se você deseja enviar mais mensagens, selecione o plano que deseja fazer atualizar no botão abaixo.
                                                    Para aprender a atualizar seu plano, assista a este vídeo no YouTube:👇\n{upgrade_youtube_url}
                                                    Além disso, também preparamos um artigo que pode ser útil para você. Para acessar o artigo, visite este link:👇\n{upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Spanish':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/es-LA/support/solutions/articles/150000079074-c%C3%B3mo-adquirir-nuestros-planes-en-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Ha finalizado el número máximo de mensajes que puede enviar este mes.
                                                    Tu plan es {plan} plan.
                                                    Si desea enviar más mensajes, selecciona el plan que deseas actualizar en el botón de abajo.
                                                    Además, hemos preparado un artículo que podría ser útil para ti. Para acceder al artículo, visita este enlace:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Tagalog':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/fil/support/solutions/articles/150000079074-paano-bumili-ng-aming-mga-plano-sa-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Ang maximum na bilang ng mga mensahe na maaari mong ipadala ngayong buwan ay natapos na.
                                                    Ang iyong plano ay {plan} plan.
                                                    Kung nais mong magpadala ng mas maraming mga mensahe, Mangyaring piliin ang plano na nais mong i-upgrade gamit ang pindutan sa ibaba.
                                                    Karagdagan, mayroon kaming inihandang artikulo na maaaring makatulong sa iyo. Para ma-access ang artikulo, bisitahin ang link na ito:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Vietnamese':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/vi/support/solutions/articles/150000079074-c%C3%A1ch-%C4%91%E1%BB%83-mua-c%C3%A1c-g%C3%B3i-c%E1%BB%A7a-ch%C3%BAng-t%C3%B4i-tr%C3%AAn-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Số tin nhắn tối đa bạn có thể gửi trong tháng này đã hết.
                                                    Gói của bạn là gói {plan}.
                                                    Nếu bạn muốn gửi thêm tin nhắn, vui lòng chọn gói mà bạn muốn nâng cấp bằng cách sử dụng nút bên dưới.
                                                    Ngoài ra, chúng tôi đã chuẩn bị một bài viết có thể hữu ích cho bạn. Để truy cập bài viết, vui lòng truy cập liên kết này:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            elif user_language == 'Japanese':
                upgrade_article_url = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079074-how-to-acquire-our-plans-in-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    今月送信可能なメッセージ回数が終了しました。
                                                    あなたのプランは {plan} planです。
                                                    さらにメッセージを送信したい場合は、下のボタンからアップグレードしたいプランを選択してください。
                                                    また、アップグレード方法に関する記事は以下になります:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
            else:
                upgrade_article_url = "https://pictolang-help.freshdesk.com/en/support/solutions/articles/150000079074-how-to-acquire-our-plans-in-chatbot-pictolang-"
                text_message = TextSendMessage(text=f"""
                                                    Your maximum number of messages you can send this month has ended.
                                                    Your plan is {plan} plan.
                                                    If you want to send more messages, Please select the plan you wish to upgrade using the button below.
                                                    In addition, we've prepared an article that might be helpful to you. To access the article, visit this link:👇
                                                    {upgrade_article_url}
                                                    """, quick_reply=quick_reply)
 
            # Push the message to the user
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            from linebot.exceptions import LineBotApiError
            try:
                line_bot_api.reply_message(reply_token, [text_message, flex_message])
            except LineBotApiError as e:
                print("Error:", e)