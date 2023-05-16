def basic_plan_component(basic_plan_url,user_language):
    if user_language == 'Portuguese':
        text = "100 mensagens por 80 ienes mensais"
    elif user_language == 'Spanish':
        text = "100 mensajes por 80 yenes mensuales"
    elif user_language == 'Tagalog':
        text = "100 mensahe para sa 80 yen buwan-buwan"
    elif user_language == 'Vietnamese':
        text = "100 tin nhắn với giá 80 yên hàng tháng"
    elif user_language == 'Japanese':
        text = "月額80円で月に100回メッセージを送信可能"
    else:
        text = "100 messages for 80 yen monthly"

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
        text = "300 mensagens por 230 ienes mensais"
    elif user_language == 'Spanish':
        text = "300 mensajes por 230 yenes mensuales"
    elif user_language == 'Tagalog':
        text = "300 mensahe para sa 230 yen buwan-buwan"
    elif user_language == 'Vietnamese':
        text = "300 tin nhắn với giá 230 yên hàng tháng"
    elif user_language == 'Japanese':
        text = "月額230円で月に300回メッセージを送信可能"
    else:
        text = "300 messages for 230 yen monthly"
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
        text = "Mensagens ilimitadas por 750 ienes mensais"
    elif user_language == 'Spanish':
        text = "Mensajes ilimitados por 750 yenes mensuales"
    elif user_language == 'Tagalog':
        text = "Walang limitasyong mga mensahe para sa 750 yen bawat buwan"
    elif user_language == 'Vietnamese':
        text = "Tin nhắn không giới hạn với 750 yên hàng tháng"
    elif user_language == 'Japanese':
        text = "月額750円で無制限にメッセージを送信可能"
    else:
        text = "Unlimited messages for 750 yen monthly"
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
        text = "100 mensagens por 80 ienes mensais"
        text_send = "Quero assinar o basic plan"
    elif user_language == 'Spanish':
        text = "100 mensajes por 80 yenes mensuales"
        text_send = "Quiero suscribirme al basic plan"
    elif user_language == 'Tagalog':
        text = "100 mensahe para sa 80 yen buwan-buwan"
        text_send = "Gusto kong mag-subscribe sa basic plan"
    elif user_language == 'Vietnamese':
        text = "100 tin nhắn với giá 80 yên hàng tháng"
        text_send = "Tôi muốn đăng ký basic plan"
    elif user_language == 'Japanese':
        text = "月額80円で月に100回メッセージを送信可能"
        text_send = "basic planを契約したいです。"
    else:
        text = "100 messages for 80 yen monthly"
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
        text = "300 mensagens por 230 ienes mensais"
        text_send = "Quero assinar o standard plan"
    elif user_language == 'Spanish':
        text = "300 mensajes por 230 yenes mensuales"
        text_send = "Quiero suscribirme al standard plan"
    elif user_language == 'Tagalog':
        text = "300 mensahe para sa 230 yen buwan-buwan"
        text_send = "Gusto kong mag-subscribe sa standard plan"
    elif user_language == 'Vietnamese':
        text = "300 tin nhắn với giá 230 yên hàng tháng"
        text_send = "Tôi muốn đăng ký standard plan"
    elif user_language == 'Japanese':
        text = "月額230円で月に300回メッセージを送信可能"
        text_send = "standard planを契約したいです。"
    else:
        text = "300 messages for 230 yen monthly"
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
        text = "Mensagens ilimitadas por 750 ienes mensais"
        text_send = "Quero assinar o premium plan"
    elif user_language == 'Spanish':
        text = "Mensajes ilimitados por 750 yenes mensuales"
        text_send = "Quiero suscribirme al premium plan"
    elif user_language == 'Tagalog':
        text = "Walang limitasyong mga mensahe para sa 750 yen bawat buwan"
        text_send = "Gusto kong mag-subscribe sa premium plan"
    elif user_language == 'Vietnamese':
        text = "Tin nhắn không giới hạn với 750 yên hàng tháng"
        text_send = "Tôi muốn đăng ký premium plan"
    elif user_language == 'Japanese':
        text = "月額750円で無制限にメッセージを送信可能"
        text_send = "premium planを契約したいです。"
    else:
        text = "Unlimited messages for 750 yen monthly"
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