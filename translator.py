# translator implementation
import requests


# translate text in language
class Translator:

    # translator initialization method
    def __init__(self, key):
        self.key = key
        self.api_url = 'https://translate.yandex.net/api/v1.5/tr.json/'

    # detect language method
    def detect_language(self, text):
        method = 'detect'
        data = {'key': self.key,
                  'text': text}
        response = requests.post(self.api_url + method, data = data)
        return response.json()['lang']

    # translate method
    def translate_text(self, text, lang):
        method = 'translate'
        data = {'key': self.key,
                'text': text,
                'lang': lang}
        response = requests.post(self.api_url + method, data = data)
        return response.json()['text']
