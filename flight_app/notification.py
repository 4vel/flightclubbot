import logging
import requests

logging.basicConfig(level=logging.INFO)


class NotificationManager:
    """ Отвечает за отправку сообщений о найденных билетах"""

    def __init__(self, BOT_TOKEN):
        self.token = BOT_TOKEN
        self.chat_id = None

    def check_message_duplicates(self):
        """ Проверяет наличие таких же сообщений в отправленных ранее """
        pass

    def add_message_to_db(self):
        """Добавляет сообщения в базу"""
        pass

    def send_sms(self, message='bla-bla-bla'):
        """ Отправляет сообщения юзерам """

        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {'chat_id': self.chat_id, 'text': message}
        r = requests.post(url, json = payload)
        return r

