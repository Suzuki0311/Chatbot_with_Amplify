def basic_plan_component(basic_plan_url):
    return {
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
    }


def standard_plan_component(standard_plan_url):
    return {
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
    }


def premium_plan_component(premium_plan_url):
    return {
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