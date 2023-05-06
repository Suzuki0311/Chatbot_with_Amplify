def basic_plan_component(basic_plan_url,user_language):
    if user_language == 'Portuguese':
        text = "100 mensagens por mês por 80 yen por mês"
    elif user_language == 'Spanish':
        text = "100 mensajes por mes por 80 yenes por mes"
    elif user_language == 'Tagalog':
        text = "100 mensahe bawat buwan para sa 80 yen bawat buwan"
    elif user_language == 'Vietnamese':
        text = "100 tin nhắn mỗi tháng với 80 yên mỗi tháng"
    elif user_language == 'Japanese':
        text = "月額80円で月に100回メッセージを送信可能"
    else:
        text = "100 messages per month for 80 yen per month"

    return {
        "type": "box",
        "layout": "vertical",
        "spacing": "none",
        "margin": "md", 
        "contents": [
            {
                "type": "text",
                "text": "basic plan",
                "size": "sm",
                "wrap": True,
            },
            {
                "type": "text",
                "text": text,
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
                    "label": "basic plan",
                    "uri": basic_plan_url
                }
            }
        ]
    }


def standard_plan_component(standard_plan_url,user_language):
    if user_language == 'Portuguese':
        text = "300 mensagens por mês por 230 yen por mês"
    elif user_language == 'Spanish':
        text = "300 mensajes por mes por 230 yenes por mes"
    elif user_language == 'Tagalog':
        text = "300 mensahe bawat buwan para sa 230 yen bawat buwan"
    elif user_language == 'Vietnamese':
        text = "300 tin nhắn mỗi tháng với 230 yên mỗi tháng"
    elif user_language == 'Japanese':
        text = "月額230円で月に300回メッセージを送信可能"
    else:
        text = "300 messages per month for 230 yen per month"
    return {
        "type": "box",
        "layout": "vertical",
        "spacing": "none",
        "margin": "md", 
        "contents": [
            {
                "type": "text",
                "text": "standard plan",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "text",
                "text": text,
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
                    "label": "standard plan",
                    "uri": standard_plan_url
                }
            }
        ]
    }


def premium_plan_component(premium_plan_url,user_language):
    if user_language == 'Portuguese':
        text = "Mensagens ilimitadas por 750 yen por mês"
    elif user_language == 'Spanish':
        text = "Mensajes ilimitados por 750 yen al mes"
    elif user_language == 'Tagalog':
        text = "Walang limitasyong mga mensahe sa halagang 750 yen bawat buwan"
    elif user_language == 'Vietnamese':
        text = "Tin nhắn không giới hạn với giá 750 yên mỗi tháng"
    elif user_language == 'Japanese':
        text = "月額750円で無制限にメッセージを送信可能"
    else:
        text = "Unlimited messages for 750 yen per month"
    return {
        "type": "box",
        "layout": "vertical",
        "spacing": "none",
        "margin": "md", 
        "contents": [
            {
                "type": "text",
                "text": "premium plan",
                "size": "sm",
                "wrap": True
            },
            {
                "type": "text",
                "text": text,
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
                    "label": "premium plan",
                    "uri": premium_plan_url
                }
            }
        ]
    }


def basic_plan_component_upgrade(user_language):
    if user_language == 'Portuguese':
        text = "100 mensagens por mês por 80 yen por mês"
        text_send = "Quero assinar o basic plan"
    elif user_language == 'Spanish':
        text = "100 mensajes por mes por 80 yenes por mes"
        text_send = "Quiero suscribirme al basic plan"
    elif user_language == 'Tagalog':
        text = "100 mensahe bawat buwan para sa 80 yen bawat buwan"
        text_send = "Gusto kong mag-subscribe sa basic plan"
    elif user_language == 'Vietnamese':
        text = "100 tin nhắn mỗi tháng với 80 yên mỗi tháng"
        text_send = "Tôi muốn đăng ký basic plan"
    elif user_language == 'Japanese':
        text = "月額80円で月に100回メッセージを送信可能"
        text_send = "basic planを契約したいです。"
    else:
        text = "100 messages per month for 80 yen per month"
        text_send = "I want to subscribe to the basic plan"
    return {
        "type": "box",
        "layout": "vertical",
        "spacing": "none",
        "margin": "md", 
        "contents": [
            {
                "type": "text",
                "text": "basic plan",
                "size": "sm",
                "wrap": True,
            },
            {
                "type": "text",
                "text": text,
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
                    "type": "message",
                    "label": "basic plan",
                    "text": text_send
                }
            }
        ]
    }

def standard_plan_component_upgrade(user_language):
    if user_language == 'Portuguese':
        text = "300 mensagens por mês por 230 yen por mês"
        text_send = "Quero assinar o standard plan"
    elif user_language == 'Spanish':
        text = "300 mensajes por mes por 230 yenes por mes"
        text_send = "Quiero suscribirme al standard plan"
    elif user_language == 'Tagalog':
        text = "300 mensahe bawat buwan para sa 230 yen bawat buwan"
        text_send = "Gusto kong mag-subscribe sa standard plan"
    elif user_language == 'Vietnamese':
        text = "300 tin nhắn mỗi tháng với 230 yên mỗi tháng"
        text_send = "Tôi muốn đăng ký standard plan"
    elif user_language == 'Japanese':
        text = "月額230円で月に300回メッセージを送信可能"
        text_send = "standard planを契約したいです。"
    else:
        text = "300 messages per month for 230 yen per month"
        text_send = "I want to subscribe to the standard plan"
    return {
    "type": "box",
    "layout": "vertical",
    "spacing": "none",
    "margin": "md", 
    "contents": [
        {
            "type": "text",
            "text": "standard plan",
            "size": "sm",
            "wrap": True
        },
        {
            "type": "text",
            "text": text,
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
                "type": "message",
                "label": "standard plan",
                "text": text_send
            }
        }
    ]
}

def premium_plan_component_upgrade(user_language):
    if user_language == 'Portuguese':
        text = "Mensagens ilimitadas por 750 yen por mês"
        text_send = "Quero assinar o premium plan"
    elif user_language == 'Spanish':
        text = "Mensajes ilimitados por 750 yen al mes"
        text_send = "Quiero suscribirme al premium plan"
    elif user_language == 'Tagalog':
        text = "Walang limitasyong mga mensahe sa halagang 750 yen bawat buwan"
        text_send = "Gusto kong mag-subscribe sa premium plan"
    elif user_language == 'Vietnamese':
        text = "Tin nhắn không giới hạn với giá 750 yên mỗi tháng"
        text_send = "Tôi muốn đăng ký premium plan"
    elif user_language == 'Japanese':
        text = "月額750円で無制限にメッセージを送信可能"
        text_send = "premium planを契約したいです。"
    else:
        text = "Unlimited messages for 750 yen per month"
        text_send = "I want to subscribe to the premium plan"
    return {
    "type": "box",
    "layout": "vertical",
    "spacing": "none",
    "margin": "md", 
    "contents": [
        {
            "type": "text",
            "text": "premium plan",
            "size": "sm",
            "wrap": True
        },
        {
            "type": "text",
            "text": text,
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
                "type": "message",
                "label": "premium plan",
                "text": text_send
            }
        }
    ]
}