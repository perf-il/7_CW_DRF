import requests

from users.models import User

URL = 'https://api.telegram.org/bot6608247362:AAEttN7EpjQ02hdVGE7z3jTi97BzWBZfLzQ/'


def ping_bot():
    method = 'getUpdates'
    response = requests.get(URL + method)
    id_users = set()
    for result in response.json().get('result'):
        chat_id = result['message']['from']['id']
        id_users.add(chat_id)
        # answer = requests.get(URL + f'sendMessage?chat_id={chat_id}&text=привет')
    for id_user in id_users:
        if not User.objects.filter(tg_user_id=id_user).exists():
            pass

    # return response.json().get('result')
    return id_users


print(ping_bot())
