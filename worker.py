"""
worker -- запускаемый воркер

created by pavel in pavel as 10/2/19
Проект evecrab
"""
from time import sleep
import datetime
from core import get_settings
import csv

from core.crawlers import BaseTelegramCrawler, UploadTelegramCrawler
from core.detector import AlgorithmicFilter

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'


CYCLE_SLEEP_TIME = 60


# Список каналов
CHANNELS_LIST = [
    'https://t.me/TG_security',
    'https://t.me/haccking',
    'https://t.me/webware',
    'https://t.me/exploitex',
    'https://t.me/hackerlib',
    'https://t.me/SecLabNews',
    'https://t.me/alexmakus',
    'https://t.me/anti_malware',
    'https://t.me/certkznews',
    'https://t.me/plastikcash',
    'https://t.me/thehaking',
    'https://t.me/sterkin_ru',
    'https://t.me/it_ha',
    'https://t.me/Russian_OSINT',
    'https://t.me/overlamer1',
    'https://t.me/bugfeature',
    'https://t.me/deeptoweb',
    'https://t.me/HNews'
]

# Чат, в который мы будем отправлять сообщение
CHAT_TO_SEND = get_settings()['chat_to_send_events_id']


def one_cycle():
    crawler = BaseTelegramCrawler('', '')
    for chanel in CHANNELS_LIST:
        for message in crawler(chanel):
            # Инициализация детектора и передача текста детектору
            detector = AlgorithmicFilter(message)
            # Определение текста на начиличие заданных тем
            is_IS_event = detector.detect_event(True) and detector.detect_is(True)
            if is_IS_event:
                # Отправка сообщения в заданный чат
                crawler.send_message_to_chat(CHAT_TO_SEND, detector.message)


def channels_to_csv():
    """
    Функция, записывающая данные с Telegram-канала в csv файл
    """
    for chanel in CHANNELS_LIST:
        with UploadTelegramCrawler(chanel, 'data/') as crawler:
            crawler.upload_to_csv()


def main():
    print(datetime.datetime.now())

    while True:
        one_cycle()
        # channels_to_csv()
        sleep(CYCLE_SLEEP_TIME)


if __name__ == "__main__":
    main()
