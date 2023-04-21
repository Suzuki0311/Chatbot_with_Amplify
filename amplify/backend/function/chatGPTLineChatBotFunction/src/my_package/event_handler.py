import json
from linebot.models import FlexSendMessage, QuickReply
from linebot import LineBotApi
from . import db_accessor
from . import line_api
from . import guard
from . import message_repository
from line_request_body_parser import extract_info_from_event_body, get_quick_reply_text
from language_codes import language_code_to_name
from image_processing import process_image
from quick_reply_buttons import create_quick_reply_buttons

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
