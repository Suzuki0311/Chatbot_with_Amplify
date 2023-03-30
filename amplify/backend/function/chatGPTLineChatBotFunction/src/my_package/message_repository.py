import uuid
from datetime import datetime

# import chatgpt_api
# import db_accessor
# import message_repository
from . import chatgpt_api
from . import db_accessor
from . import message_repository
from . import index


QUERY_LIMIT = 5


def _fetch_chat_histories_by_line_user_id(line_user_id, prompt_text):
    try:
        if line_user_id is None:
            raise Exception('To query an element is none.')

        # Query messages by Line user ID.
        db_results = db_accessor.query_by_line_user_id(line_user_id, QUERY_LIMIT)
        print("db_results:",db_results)

        # Reverse messages
        reserved_results = list(reversed(db_results))
        print("reserved_results:",reserved_results)

        # Create new dict list of a prompt
        chat_histories = list(map(lambda item: {"role": item["role"]["S"], "content": item["content"]["S"]}, reserved_results))
        print("chat_histories:",chat_histories)
        # Create the list of a current user prompt
        if index.message_image_id != None:
            current_prompts = [{"role": "system", "content": "you are an excellent writer"},
                               {"role": "user", "content": prompt_text}]
        else:
            current_prompts = [{"role": "user", "content": prompt_text}]
        print("current_prompts:",current_prompts)

        # Join the lists
        print("chat_histories + current_prompts:",chat_histories + current_prompts)
        return chat_histories + current_prompts

    except Exception as e:
        # Raise the exception
        raise e


def _insert_message(line_user_id, role, prompt_text):
    try:
        if prompt_text is None or role is None or line_user_id is None:
            raise Exception('To insert elements are none.')

        # Create a partition key
        partition_key = str(uuid.uuid4())

        # Put a record of the user into the Messages table.
        db_accessor.put_message(partition_key, line_user_id, role, prompt_text, datetime.now())

    except Exception as e:
        # Raise the exception
        raise e


def create_completed_text(line_user_id, prompt_text):
    # Query messages by Line user ID.
    chat_histories = message_repository._fetch_chat_histories_by_line_user_id(line_user_id, prompt_text)
    print("chat_histories:",chat_histories)

    # Call the GPT3 API to get the completed text
    completed_text = chatgpt_api.completions(chat_histories)
    print("completed_text:",completed_text)

    # Put a record of the user into the Messages table.
    message_repository._insert_message(line_user_id, 'user', prompt_text)

    # Put a record of the assistant into the Messages table.
    message_repository._insert_message(line_user_id, 'assistant', completed_text)

    return completed_text