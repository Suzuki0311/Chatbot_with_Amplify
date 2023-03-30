import json

# import guard
# import line_api
# import line_request_body_parser
# import message_repository

import sys
print("sys.path:", sys.path)


from . import guard
from . import line_api
from . import line_request_body_parser
from . import message_repository
from linebot import LineBotApi
from linebot.models import TextSendMessage
from . import const
import io
from google.oauth2 import service_account
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import translate_v2

def handler(event, context):
    try:
        # Verify if the request is valid
        guard.verify_request(event)

        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

        # Parse the event body as a JSON object
        # Test_after remove text
        event_body = json.loads(event['body'])
        print("event_body:",event_body)
        prompt_text = line_request_body_parser.get_prompt_text(event_body)
        print("prompt_text:",prompt_text)
        line_user_id = line_request_body_parser.get_line_user_id(event_body)
        print("line_user_id:",line_user_id)
        reply_token = line_request_body_parser.get_reply_token(event_body)
        print("reply_token:",reply_token)
        message_image_id = line_request_body_parser.get_image_content(event_body)
        print("message_image_id:",message_image_id)
        if message_image_id != None:
            # Create an instance of the LineBotApi with the Line channel access token
            language_code_to_name = {
                'en': 'English',
                'ja': 'Japanese',
                'zh': 'Chinese',
                'es': 'Spanish',
                'fr': 'French',
                'zh': 'Chinese',
                'zh-CN': 'Chinese（Simplified Chinese）',
                'zh-TW': 'Chinese（Traditional Chinese）',
                'en-US': 'English',
                'en-GB': 'English',
                'en-CA': 'English',
                'en-AU': 'English',
                'fr-CA': 'French',
                'de': 'German',
                'it': 'Italian',
                'ko': 'Korean',
                'pt': 'Portuguese',
                'pt-PT': 'Portuguese',
                'pt-BR': 'Portuguese',
                'th': 'Thai',
                'vi': 'Vietnamese'
                    # 他の言語コードと名前を追加
                }
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)
            print("line_bot_api:",line_bot_api)
            message_image_content = line_bot_api.get_message_content(message_image_id)
            print("message_image_content:",message_image_content)
            image_bytes = io.BytesIO(message_image_content.content)
            print("image_bytes:",image_bytes)
            service_account_info = json.loads(const.GOOGLE_APPLICATION_CREDENTIALS)
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            client = vision.ImageAnnotatorClient(credentials=credentials)
            print("client:",client)
            image = vision.Image(content=image_bytes.getvalue())
            print("image:",image)
            response = client.document_text_detection(image=image)
            print("response:",response)
            target_sentence = response.full_text_annotation.text
            print("target_sentence:",target_sentence)
            translate_client = translate_v2.Client(credentials=credentials)
            text_language = translate_client.detect_language(target_sentence)
            text_language = language_code_to_name[text_language['language']]
            print("text_language:",text_language)


        # Check if the event is a message type and is of text type
        if prompt_text is None or line_user_id is None or reply_token is None:
            raise Exception('Elements of the event body are not found.')

        print(prompt_text.replace('\n', ''))

        # Create the completed text by Chat-GPT 3.5 turbo
        completed_text = message_repository.create_completed_text(line_user_id, prompt_text)
        print("completed_text:",completed_text)
        # Reply the message using the LineBotApi instance
        line_api.reply_message_for_line(reply_token, completed_text)

    except Exception as e:
        # Log the error
        print(e)

        # Return 200 even when an error occurs as mentioned in Line API documentation
        # https://developers.line.biz/ja/reference/messaging-api/#response
        return {'statusCode': 200, 'body': json.dumps(f'Exception occurred: {e}')}

    # Return a success message if the reply was sent successfully
    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}