"""
worker -- запускаемый воркер
"""
from time import sleep
import datetime
from core import get_settings
from core.crawlers import BaseTelegramCrawler, UploadTelegramCrawler
from core.detector import AlgorithmicFilter


CYCLE_SLEEP_TIME = 60

# Список каналов
CHANNELS_LIST = get_settings()['telegram_chat_links_list']

# Чат, в который мы будем отправлять сообщение
CHAT_TO_SEND = get_settings()['chat_id_to_send_events']


def one_cycle():
    crawler = BaseTelegramCrawler()
    for chanel in CHANNELS_LIST:
        crawler.set_base_url(chanel)
        for message in crawler.get_messages():
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
