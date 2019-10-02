"""
core/.__init__.py

Ядро системы.

created by pavel in pavel as 10/2/19
Проект evecrab
"""
import os
import datetime

# __author__ = 'pavelmstu'
# __maintainer__ = 'pavelmstu'
# __credits__ = ['pavelmstu', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'

# Путь к проекту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Message:
    """
    Сообщение, содержащее информацию о событии
    """

    def __init__(self, url, short_description, long_description=None, datetime_ = None):

        self.url = url
        self.short_description = short_description
        self.long_description = long_description
        if datetime_:
            self.datetime_ = datetime_
        else:
            self.datetime_ = datetime.datetime.now()

        assert isinstance(self.datetime_, datetime.datetime)
        assert isinstance(self.url, str)
        assert isinstance(self.short_description, str)
        assert isinstance(self.long_description, str) or self.long_description is None


def get_settings():
    """
    Функция, возвращающая словарь settings,
        выбирая данные из ~/settings/private.json и ~/settings/public.json
    :return:
    """
    if not os.path.exists(os.path.join(BASE_DIR, 'settings', 'public.json')):
        raise EnvironmentError(
            "Нет файла ~/settings/private.json! Создайте его, скопировав Нет файла ~/settings/private.example.json"
        )

    settings = dict()
    # TODO ~/settings/private.json
    # TODO ~/settings/public.json
    raise NotImplementedError("Функция core.get_settings не написана!")
    return settings
