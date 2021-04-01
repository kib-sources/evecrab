"""

core.crawlers -- модуль, содержащий основные базовые краулеры

created by pavel in pavel as 10/2/19
Проект evecrab
"""
from _datetime import date
from core import Message
from core import get_settings
import csv

from telethon.sync import TelegramClient


# __author__ = 'pavel'
# __maintainer__ = 'pavel'
# __credits__ = ['pavel', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'


class BaseCrawler:
    """
    Абстрактный класс базового краулера
    """

    def __init__(self, base_url, base_account_folder):

        # Базовый урл, который парсится
        self.base_url = base_url

        # Базовая папка, куда будут складироватся логи и информация об уже обработанных страницах
        self.base_account_folder = base_account_folder


class BaseTelegramCrawler(BaseCrawler):
    """
    Базовый краулер для телеграмм-каналов
    """

    def __init__(self, base_url, base_account_folder, limit=1000):
        super().__init__(base_url, base_account_folder)

        # Устанавливаем лимит получаемых сообщений
        self.limit = limit

        # Получаем необходимые настройки
        _settings = get_settings()

        # Присваиваем значения внутренним переменным
        _api_id = _settings['api_id']
        _api_hash = _settings['api_hash']
        _username = _settings['username']

        # Создадим объект клиента Telegram API
        self.client = TelegramClient(_username, _api_id, _api_hash)

        # Запускаем клиент
        self.client.start()

    def __iter__(self):
        """
        Возвращаем экземпляр класса Message при итерировании
        :return:
        """
        for message in self.client.iter_messages(self.base_url, limit=self.limit):
            yield Message(self.base_url, message.text, datetime_=message.date)

    def __call__(self, url):
        """
        Передаем ссылку на обрабатываемый url при вызове экземпляра класса
        :param url:
        :return: self
        """
        self.base_url = url
        return self

    # Функция для отправки сообщения в определенный чат
    def send_message_to_chat(self, chat, message):
        self.client.send_message(chat, message.description)


class UploadTelegramCrawler(BaseCrawler):
    """
    Краулер, выгружающий данные из телеграмм-каналов
    """

    def __init__(self, base_url, base_account_folder, limit=1000):
        super().__init__(base_url, base_account_folder)

        self.limit = limit

        # Получаем необходимые настройки
        _settings = get_settings()

        # Присваиваем значения внутренним переменным
        _api_id = _settings['api_id']
        _api_hash = _settings['api_hash']
        _username = _settings['username']

        # Создадим объект клиента Telegram API
        self.client = TelegramClient(_username, _api_id, _api_hash)

        print('Вызвали конструктор')

    def __enter__(self):
        print("Вызвали enter")
        # Запускаем клиент
        self.client.start()

        return self

    def __exit__(self, type, value, traceback):
        print('Вызвали exit')
        self.client.disconnect()

    def __iter__(self):
        """
        Возвращаем экземпляр класса Message при итерировании
        :return:
        """
        print(self.base_url)
        for message in self.client.iter_messages(self.base_url, limit=self.limit):
            yield Message(self.base_url, message.text, datetime_=message.date)

    def upload_to_csv(self):

        # Поля таблицы
        field_names = ['Text', 'Date']

        # Открываем csv файл
        with open(self.base_account_folder + self.base_url.split('/')[-1] + '.csv', 'w', encoding='utf-8') as csv_file:
            # Инициализация экземляра DictWriter
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
            csv_writer.writeheader()

            # Итерируемся по сообщениям
            for message in self:
                if message.description:
                    # Записываем один ряд таблицы
                    csv_writer.writerow({'Text': message.description, 'Date': message.datetime_})





