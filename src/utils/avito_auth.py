import requests
import logging
import os
import json
from dotenv import load_dotenv

logging.basicConfig(filename='avito_auth_logger.log',
                    encoding='utf-8',
                    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
                    level=logging.INFO)

load_dotenv()
USER_ID = os.getenv('USER_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_auth_key():
    uri = "https://api.avito.ru/token/"

    request_data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    try:
        response = requests.post(uri, data=request_data)
        json.dump(response.json(), open('auth_key.json', 'w'), indent=2)
    except Exception as e:
        logging.error(e)


def set_webhook(token: str):
    uri = 'https://api.avito.ru/messenger/v2/webhook'
    header = {
        "Authorization": f"Bearer {token}"
    }
    request_data = {
        "url": "tmp"
    }
    try:
        requests.post(uri, headers=header, json=request_data)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    get_auth_key()
    auth_response = json.load(open('auth_key.json', 'r'))
    auth_key = auth_response.get('access_token')
    if auth_key:
        set_webhook(auth_key)
