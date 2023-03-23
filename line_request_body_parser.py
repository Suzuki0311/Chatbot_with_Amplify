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