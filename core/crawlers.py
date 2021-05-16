"""
core.crawlers -- модуль, содержащий основные базовые краулеры
"""

from core import Message
from core import get_settings
import csv
from telethon.sync import TelegramClient


class BaseCrawler:
    """
    Абстрактный класс базового краулера
    """

    def __init__(self, base_url='', base_account_folder=''):

        # Базовый урл, который парсится
        self.base_url = base_url

        # Базовая папка, куда будут складироватся логи и информация об уже обработанных страницах
        self.base_account_folder = base_account_folder


class BaseTelegramCrawler(BaseCrawler):
    """
    Базовый краулер для телеграмм-каналов
    """

    def __init__(self, base_url='', base_account_folder='', limit=1000):
        super().__init__(base_url, base_account_folder)

        # Устанавливаем лимит получаемых с канала сообщений
        self.limit = limit

        # Получаем необходимые настройки
        _settings = get_settings()

        # Присваиваем значения настроек внутренним переменным
        _api_id = _settings['api_id']
        _api_hash = _settings['api_hash']
        _username = _settings['username']

        # Создаем объект клиента Telegram API
        self.client = TelegramClient(_username, _api_id, _api_hash)

        # Запускаем клиент
        self.client.start()

    def set_base_url(self, url):
        """
        Метод, устанавлявающий базовый урл, который парсится
        :param url:
        :return:
        """
        self.base_url = url

    def get_messages(self):
        """
        Возвращаем экземпляр класса Message при итерировании
        :return: Message
        """

        for message in self.client.iter_messages(self.base_url, limit=self.limit):
            yield Message(self.base_url, message.text, datetime_=message.date)

    # Функция для отправки сообщения в определенный чат
    def send_message_to_chat(self, chat, message):
        self.client.send_message(chat, message.description)


class UploadTelegramCrawler(BaseCrawler):
    """
    Краулер, выгружающий данные из телеграмм-каналов
    """

    def __init__(self, base_url, base_account_folder, limit=1000):
        super().__init__(base_url, base_account_folder)

        # Устанавливаем лимит получаемых с канала сообщений
        self.limit = limit

        # Получаем необходимые настройки
        _settings = get_settings()

        # Присваиваем значения внутренним переменным
        _api_id = _settings['api_id']
        _api_hash = _settings['api_hash']
        _username = _settings['username']

        # Создадим объект клиента Telegram API
        self.client = TelegramClient(_username, _api_id, _api_hash)

    def __enter__(self):
        # Запускаем клиент
        self.client.start()
        return self

    def __exit__(self, type, value, traceback):
        """
        Отключаем клиента
        :param type:
        :param value:
        :param traceback:
        :return:
        """
        self.client.disconnect()

    def get_messages(self):
        """
        Возвращаем экземпляр класса Message при итерировании
        :return: Message
        """

        for message in self.client.iter_messages(self.base_url, limit=self.limit):
            yield Message(self.base_url, message.text, datetime_=message.date)

    def upload_to_csv(self):

        # Поля таблицы
        field_names = ['Text', 'Date']

        # Путь к csv файлу
        csv_path = self.base_account_folder + self.base_url.split('/')[-1] + '.csv'

        # Открываем csv файл
        with open(csv_path, 'w', encoding='utf-8') as csv_file:

            # Инициализация экземляра DictWriter
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

            csv_writer.writeheader()

            # Итерируемся по сообщениям
            for message in self.get_messages():
                if message.description:
                    # Записываем один ряд таблицы
                    csv_writer.writerow({'Text': message.description, 'Date': message.datetime_})





