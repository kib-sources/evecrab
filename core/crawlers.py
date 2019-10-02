"""

core.crawlers -- модуль, содержащий основные базовые краулеры

created by pavel in pavel as 10/2/19
Проект evecrab
"""
import datetime
from core import Message

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

    def _get_one(self):
        """
        Возвращает Message или None, если закончились данные
        :return:
        """
        return NotImplemented

    def __iter__(self):
        while True:
            message = self._get_one()
            if message is None:
                break
            assert isinstance(message, Message)
            yield message


class BaseHttpCrawler(BaseCrawler):
    """
    Базовый краулер для HTML страниц
    """
    # TODO


class BaseTelegramCrawler(BaseCrawler):
    """
    Базовый краулер для телеграмм-каналов
    """
    # TODO


class BaseVkCrawler(BaseCrawler):
    """
    Базовый краулер для вК
    """
    # TODO
