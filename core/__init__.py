"""
core/.__init__.py
Ядро системы.
"""
import os
import datetime
import json

# Путь к проекту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Относительный путь к данным из public.json
PUBLIC_SETTINGS_PATH = '/settings/public.json'

# Относительный путь к данным из private.json
PRIVATE_SETTINGS_PATH = '/settings/private.json'

# Относительный путь к ИБ-словарю is_words.json
IS_DICT_PATH = 'dictionaries/is_words.json'

# Относительный путь к Event-словарю events_words.json
EVENTS_DICT_PATH = 'dictionaries/events_words.json'


class Message:
    """
    Сообщение, содержащее информацию о событии
    """
    def __init__(self, url, description, datetime_=None):

        self.url = url
        self.description = description
        if datetime_:
            self.datetime_ = datetime_
        else:
            self.datetime_ = datetime.datetime.now()

        assert isinstance(self.datetime_, datetime.datetime)
        assert isinstance(self.url, str)
        # assert isinstance(self.description, str)


def get_settings():
    """
    Функция, возвращающая словарь settings,
    выбирая данные из ~/settings/private.json и ~/settings/public.json
    :return:
    """
    if not os.path.exists(os.path.join(BASE_DIR, 'settings', 'public.json')):
        raise EnvironmentError(
            "Нет файла ~/settings/private.json! Создайте его, скопировав ~/settings/private.example.json"
        )
    settings = dict()

    # Считываем данные из ~/settings/public.json
    with open(BASE_DIR + PUBLIC_SETTINGS_PATH, "r") as read_json_file:
        public_settings = json.load(read_json_file)

    # Считываем данные из ~/settings/private.json
    with open(BASE_DIR + PRIVATE_SETTINGS_PATH, "r") as read_json_file:
        private_settings = json.load(read_json_file)

    # Необходимые ключи из public.json
    keys_from_public = ['telegram_chat_links_list']

    # Необходимые ключи из private.json
    keys_from_private = ['api_id', 'api_hash', 'username', 'bot_token',
                         'chat_id_to_send_events', 'chat_id_to_send_polls_results',
                         'chat_id_to_send_polls']

    # Добавление необходимых настроек в словарь
    settings.update({key: private_settings[key] for key in keys_from_private})
    settings.update({key: public_settings[key] for key in keys_from_public})

    return settings


def get_is_set():
    """
    Функция, возвращая множество слов по ИБ
    :return:
    """
    with open(IS_DICT_PATH) as json_file:
        data = json.load(json_file)
        return set(data['IS'])


def get_events_set():
    """
    Функция, возвращая множество слов по событиям
    :return:
    """
    with open(EVENTS_DICT_PATH) as json_file:
        data = json.load(json_file)
        return set(data['Events'])

