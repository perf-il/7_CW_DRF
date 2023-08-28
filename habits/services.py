import requests

from config.settings import TELEGRAM_BOT_TOKEN

URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'


def get_all_users_bot():
    method = 'getUpdates'
    response = requests.get(URL + method)
    print(response.json())
    all_users = list()
    id_users = list()
    for result in response.json().get('result'):
        user_id = result['message']['from']['id']
        user_first_name = result['message']['from']['first_name']
        user_last_name = result['message']['from']['last_name']
        user_name = result['message']['from']['username']
        if user_id not in id_users:
            id_users.append(user_id)
            all_users.append({
                'id': user_id,
                'first_name': user_first_name,
                'last_name': user_last_name,
                'username': user_name,
            })

    return all_users


def send_message_bot(chat_id, text):
    method = 'sendMessage'
    url = URL + method
    params = {
        'chat_id': chat_id,
        'text': text,
    }
    answer = requests.get(url, params=params)
    return answer.json().get('ok')
