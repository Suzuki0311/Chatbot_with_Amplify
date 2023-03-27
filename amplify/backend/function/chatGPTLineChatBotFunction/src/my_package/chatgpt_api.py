import openai
import const

# Model name
GPT3_MODEL = 'gpt-3.5-turbo'

# Maximum number of tokens to generate
MAX_TOKENS = 1024

# Create a new dict list of a system
# SYSTEM_PROMPTS = [{'role': 'system', 'content': '敬語を使うのをやめてください。友達のようにタメ口で話してください。また、絵文字をたくさん使って話してください。'}]
SYSTEM_PROMPTS = [{'role': 'system', 'content': 'Please stop using polite language. Talk to me in a friendly way like a friend. Also, use a lot of emojis when you talk.'}]


def completions(history_prompts):
    messages = SYSTEM_PROMPTS + history_prompts

    print(f"prompts:{messages}")
    try:
        openai.api_key = const.OPEN_AI_API_KEY
        response = openai.ChatCompletion.create(
            model=GPT3_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        # Raise the exception
        raise e