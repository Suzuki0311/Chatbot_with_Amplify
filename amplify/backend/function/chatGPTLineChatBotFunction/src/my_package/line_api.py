# import const
from . import const
from linebot import LineBotApi
from linebot.models import TextSendMessage

def reply_message_for_line(reply_token, completed_text, quick_reply=None):
    try:
        # Create an instance of the LineBotApi with the Line channel access token
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

        # Create a TextSendMessage with the quick_reply parameter
        text_message = TextSendMessage(text=completed_text, quick_reply=quick_reply)

        # Reply the message using the LineBotApi instance
        line_bot_api.reply_message(reply_token, text_message)

    except Exception as e:
        # Raise the exception
        raise e