import const
from linebot import LineBotApi
from linebot.models import TextSendMessage

def reply_message_for_line(reply_token, completed_text):
    try:
        # Create an instance of the LineBotApi with the Line channel access token
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

        # Reply the message using the LineBotApi instance
        line_bot_api.reply_message(reply_token, TextSendMessage(text=completed_text))

    except Exception as e:
        # Raise the exception
        raise e