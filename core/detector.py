"""
core.detector базовый модуль ЭС, обнаруживающие полезную информацию в тексте

created by pavel in pavel as 10/2/19
Проект evecrab
"""
import numpy as np
import datetime

# __author__ = 'pavel'
# __maintainer__ = 'pavel'
# __credits__ = ['pavel', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'


def split_text(text):
    text = text.replace('\n', ' ').replace('\t', ' ')

    while '  ' in text:
        text = text.replace('  ', ' ')
    return text.split(' ')


class BaseDetector:
    """
    Базовый детектор текстов
    """

    def __init__(self):
        self._text_list = list()

    def append(self, text):
        self._text_list.append(text)

    @property
    def text_list(self):
        return self._text_list[:]

    def _one_predict(self, text):
        return NotImplemented

    def predict(self):
        """
        Функция, возвращающая априорную вероятность от 0.0 до 1.0
        о том, что в тексте существует объявление о полезной информации
        :return:
        """
        if not self._text_list:
            return 0.0

        p_list = [self._one_predict(text) for text in self._text_list]
        return np.max(p_list)


class KeyWordDummyISDetector(BaseDetector):
    """
    Простой детектор, который используется для проверки элементарных гипотез
    Только после KeyWordISDummyDetector запускаются другие детекторы.
    """

    LIST_DETECT = [
        "иб",
        "информационаая безопасность",
        "information security",
        # TODO дописать слова
    ]

    def _one_predict(self, text):

        # TODO прогнать text через https://yandex.ru/dev/mystem/
        # text = ...
        for word in split_text(text):
            if word.lower() in self.LIST_DETECT:
                return 1.0
        return 0.0


class ISDetector(BaseDetector):
    """
    'Нормальный' детектор
    """
    # TODO
