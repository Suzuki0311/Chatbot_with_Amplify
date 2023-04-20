def get_prompt_text(event_body):
    if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'text':
        return event_body['events'][0]['message']['text']
    return None


def get_line_user_id(event_body):
    if event_body['events'][0]['source'] and event_body['events'][0]['source']['type'] == 'user':
        return event_body['events'][0]['source']['userId']
    return None


def get_reply_token(event_body):
    if event_body['events'][0]['replyToken']:
        return event_body['events'][0]['replyToken']
    return None

def get_image_content(event_body):
    if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'image':
        return event_body['events'][0]['message']['id']
    return None

def get_quick_reply_text(event_body):
    if "events" in event_body and len(event_body["events"]) > 0:
        event = event_body["events"][0]
        if "message" in event and "text" in event["message"]:
            if "quickReply" in event["message"]:
                return event["message"]["text"]
    return None
