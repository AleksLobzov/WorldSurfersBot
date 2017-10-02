# bot handler implementation

import requests


# bot handler class
class BotHandler:

    # bot initialization method
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    # get updates method
    def get_updates(self, timeout=30, offset=None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, data=params)
        result_json = response.json()['result']
        return result_json

    # send message method
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        response = requests.post(self.api_url + method, data=params)
        return response

    # get last update method
    def last_update(self):
        get_result = self.get_updates()
        length = len(get_result)
        last_update = get_result[length-1] if length > 0 else get_result[length]
        return last_update
