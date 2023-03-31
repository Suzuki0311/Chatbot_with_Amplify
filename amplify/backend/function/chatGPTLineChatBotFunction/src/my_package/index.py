import json
import sys
print("sys.path:", sys.path)
from . import guard
from . import line_api
from . import line_request_body_parser
from . import message_repository
from . import language_codes
from linebot import LineBotApi
from linebot.models import TextSendMessage
from . import const
import io
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

def handler(event, context):
    try:
        # Verify if the request is valid
        guard.verify_request(event)

        # Parse the event body as a JSON object
        event_body = json.loads(event['body'])
        print("event_body:",event_body)

        # Extract necessary information from event_body
        prompt_text, line_user_id, reply_token, message_image_id, profile = extract_info_from_event_body(event_body)
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