import json
import logging
import os
import requests
import yagmail
from datetime import datetime as dt

from dotenv import load_dotenv
from flask import Flask, request, make_response
from .msg_const import ANSWERS_MAPPING, DEFAULT_ANSWER


load_dotenv()
logging.basicConfig(filename='avito_logger.log',
                    filemode='a',
                    level=logging.INFO)
app = Flask(__name__)

USER_ID = os.getenv('USER_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def parse_message_txt(text: str) -> str:
    current_date = dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    logging.info('%(today)s | %(message)s', {'today': current_date, 'message': 'Start parsing message'})
    response_text = ANSWERS_MAPPING.get(text)
    if not response_text:
        current_hour = int(dt.now().strftime("%H"))
        response_pre_text = ''
        if 6 <= current_hour < 10:
            response_pre_text = 'Доброе утро. '
        elif 10 <= current_hour < 18:
            response_pre_text = 'Добрый день. '
        elif 18 <= current_hour < 0:
            response_pre_text = 'Добрый вечер. '
        elif 0 <= current_hour < 6:
            response_pre_text = 'Доброй ночи. '

        response_text = response_pre_text + DEFAULT_ANSWER

    return response_text


def send_info_email(error_message: str):
    pass


def send_message(user_id: str, chat_id: str, message: str):
    current_date = dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    url = f"https://api.avito.ru/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages"
    params = {
        "message": {
            "text": f"{message}"
        },
        "type": "text"
    }

    try:
        message_response = requests.post(url, json=params)
        logging.info('%(today)s | %(message)s', {'today': current_date,
                                                 'message': f'Message was send with response - {message_response}'})
    except Exception as e:
        logging.error('%(today)s | %(message)s', {'today': current_date, 'message': e})
        send_info_email()


@app.route('/', methods=['POST'])
def hello():
    current_date = dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    if request.method == 'POST':
        logging.info('%(today)s | %(message)s', {'today': current_date,
                                                 'message': 'Start handling POST request'})
        json_data = request.get_json()
        if json_data['payload']['type'] == 'message':
            chat_id = json_data['payload']['value']['chat_id']
            author_id = json_data['payload']['value']['author_id']
            if json_data['payload']['value']['type'] == 'text':
                message_txt = json_data['payload']['value']['content']['text']
                text_for_request = parse_message_txt(message_txt)
                # send_message(author_id, chat_id, text_for_request)
                print(text_for_request)
            else:
                text_for_request = 'Я могу отвеачть только на текстовые сообщения'
                send_message(author_id, chat_id,
                             text_for_request)  # Отправка сообщения о не поддерживаемом типе сообщений
        else:
            logging.info('%(today)s | %(message)s', {'today': current_date,
                                                     'message': 'Not message type in request'})

        logging.info('%(today)s | %(message)s', {'today': current_date, 'message': 'End handling POST request'})
    else:
        logging.warning('%(today)s | %(message)s', {'today': current_date,
                                                    'message': f'Incoming request method {request.method}, not supported'})
    return make_response()


if __name__ == '__main__':
    uri = f"https://api.avito.ru/messenger/v1/accounts/{USER_ID}/chats"
    headers = {
        "Authorization": "Bearer 6_vPhbUtSzG8JYxpYxc0LwxizL0afWORV_4vDxoG"
    }
    data = {
        "unread_only": "true",
        "limit": 50
    }
    response = requests.post('http://localhost:8765', headers=headers, json=data)
    # json.dump(response.json(), open('chats.json', 'w'), indent=3, ensure_ascii=False)
