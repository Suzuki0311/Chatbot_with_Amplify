import json
import sys
print("sys.path:", sys.path)
from . import guard
from . import event_handler

def handler(event, context):
    try:
        # Verify if the request is valid
        guard.verify_request(event)

        # Parse the event body as a JSON object
        event_body = json.loads(event['body'])
        print("event_body:", event_body)

        # Extract event type
        event_type = event_body['events'][0]['type']

        if event_type == 'follow':
            event_handler.handle_follow_event(event_body)

        elif event_type == 'message':
            event_handler.handle_message_event(event_body)

    except Exception as e:
        # Log the error
        print(e)

        # Return 200 even when an error occurs as mentioned in Line API documentation
        # https://developers.line.biz/ja/reference/messaging-api/#response
        return {'statusCode': 200, 'body': json.dumps(f'Exception occurred: {e}')}

    # Return a success message if the reply was sent successfully
    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}