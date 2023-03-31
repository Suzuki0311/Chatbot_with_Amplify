import json
import sys
print("sys.path:", sys.path)
from . import guard
from . import line_api
from . import line_request_body_parser
from . import message_repository
from . import language_codes
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from . import const
import io
from google.oauth2 import service_account
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import translate_v2

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
        return [
            QuickReplyButton(action=MessageAction(label="お問い合せ", text="お問い合せ")),
            QuickReplyButton(action=MessageAction(label="今日の献立", text="今日の献立を提案してください")),
            QuickReplyButton(action=MessageAction(label="上司へのお礼メール", text="上司へのお礼メールを書いてください"))
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
            QuickReplyButton(action=MessageAction(label="Traduzir para Japonês", text="Traduza o acima para o japonês")),
            QuickReplyButton(action=MessageAction(label="Traduzir para inglês", text="Traduza o acima para o inglês")),
            QuickReplyButton(action=MessageAction(label="Cardápio de 1 semana", text="Sugira um menu para a semana")),
            QuickReplyButton(action=MessageAction(label="Viajar para Tokyo", text="Planeje para min uma viagem para Tokyo por 3 dias e 2 noites")),
            QuickReplyButton(action=MessageAction(label="Relatório de leitura", text="Desenhe um relatório de livro para a Pedra Filosofal de Harry Potter")),
            QuickReplyButton(action=MessageAction(label="Ficar rico", text="Me diga como ficar rico")),
            QuickReplyButton(action=MessageAction(label="E-mail de agradecimento ao chefe", text="Escreva um e-mail de agradecimento ao meu chefe que cuidou de min na festa")),
            QuickReplyButton(action=MessageAction(label="Atração turística famosa do Japão", text="Diga-me algumas atrações turísticas famosas no Japão.")),
            QuickReplyButton(action=MessageAction(label="Detalhe", text="Me conte mais em detalhes")),
            QuickReplyButton(action=MessageAction(label="Aprender inglês", text="Por favor, apresente uma lista de algumas palavras essenciais em inglês para negócios e suas traduções para o português")),
            QuickReplyButton(action=MessageAction(label="Tema de pesquisa", text="Por favor, faça-me algumas perguntas e crie um tópico de pesquisa para a universidade juntos.")),
            QuickReplyButton(action=MessageAction(label="Conforte seu namorado/namorada", text="Escreva um e-mail para fazer as pazes com seu amante que brigou")),
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

def handler(event, context):
    try:
        # Verify if the request is valid
        guard.verify_request(event)

        # Parse the event body as a JSON object
        event_body = json.loads(event['body'])
        print("event_body:",event_body)

        # Extract necessary information from event_body
        prompt_text, line_user_id, reply_token, message_image_id, profile = extract_info_from_event_body(event_body)

        # Check if the event is a quick reply
        quick_reply_text = line_request_body_parser.get_quick_reply_text(event_body)
        if quick_reply_text is not None:
            prompt_text = quick_reply_text

        print("prompt_text:",prompt_text, "line_user_id:",line_user_id, "reply_token:",reply_token, "message_image_id:",message_image_id, "profile:",profile)

        # Get user's language
        user_language = language_codes.language_code_to_name[profile.language]
        print("user_language:",user_language)

        # Process image if present
        if message_image_id is not None:
            prompt_text, text_language = process_image(message_image_id)
            print("The prompt_text when image is present:",prompt_text, "text_language:",text_language)
        else:
            text_language = None

        # Check if the event is a message type and is of text type
        if prompt_text is None or line_user_id is None or reply_token is None:
            raise Exception('Elements of the event body are not found.')

        # Create the completed text by Chat-GPT 3.5 turbo
        completed_text = message_repository.create_completed_text(line_user_id, prompt_text, message_image_id, text_language, user_language)
        print("completed_text:",completed_text)

        # Create quick reply buttons
        quick_reply_buttons = create_quick_reply_buttons(user_language)
        quick_reply = QuickReply(items=quick_reply_buttons)

        # Reply the message using the LineBotApi instance with quick replies
        line_api.reply_message_for_line(reply_token, completed_text, quick_reply)

    except Exception as e:
        # Log the error
        print(e)

        # Return 200 even when an error occurs as mentioned in Line API documentation
        # https://developers.line.biz/ja/reference/messaging-api/#response
        return {'statusCode': 200, 'body': json.dumps(f'Exception occurred: {e}')}

    # Return a success message if the reply was sent successfully
    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}