import json

# import guard
# import line_api
# import line_request_body_parser
# import message_repository

from . import guard
from . import line_api
from . import line_request_body_parser
from . import message_repository


def handler(event, context):
    try:
        # Verify if the request is valid
        guard.verify_request(event)

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
        # Check if the event is a message type and is of text type
        if prompt_text is None or line_user_id is None or reply_token is None:
            raise Exception('Elements of the event body are not found.')

        print(prompt_text.replace('\n', ''))

        # Create the completed text by Chat-GPT 3.5 turbo
        completed_text = message_repository.create_completed_text(line_user_id, prompt_text)
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