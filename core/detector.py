"""
core.detector базовый модуль ЭС, обнаруживающая полезную информацию в тексте

created by pavel in pavel as 10/2/19
Проект evecrab
"""
import numpy as np
import datetime
import subprocess
from pymystem3 import Mystem

# __author__ = 'pavel'
# __maintainer__ = 'pavel'
# __credits__ = ['pavel', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'


def split_text(text):
    text = text.replace('\n', ' ').replace('\t', ' ').lower()

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

    # Словарь слов про ИБ
    LIST_DETECT_IS = [
        "иб",
        "информационный",
        "безопасность",
        "information",
        "security",
        "кибербезопасность",
        "ибспециалист",
        "уязвимость",
        "хакер",
        "проникновение"
    ]

    # Словарь слов про события
    LIST_DETECT_EVENT = [
        "интенсив",
        "курс",
        "кейс",
        "стажировка",
        "митап",
        "конференция",
        "собеседование",
        "практика",
        "собрание",
        "обучение",
        "видеоконференция"

    ]

    def _one_predict(self, text):

        # Флаги, определяющие, содержит ли данный текст информацию про ИБ и какое-либо событие
        is_IS = False
        is_event = False

        # Инициализация лемматизатора
        lemmatizer = Mystem(grammar_info=False, entire_input=False)

        # пребор всех слов
        for word in split_text(text):

            # Приведение слова к начальной форме
            norm_word = lemmatizer.lemmatize(word)
            if norm_word:
                norm_word = norm_word[0]
            else:
                continue

            # Есть ли данное слово в словаре слов про ИБ
            if norm_word in self.LIST_DETECT_IS:
                is_IS = True

            # Есть ли данное слово в словаре слов про события
            if norm_word in self.LIST_DETECT_EVENT:
                is_event = True

        return int(is_IS and is_event)


class ISDetector(BaseDetector):
    """
    'Нормальный' детектор
    """
    # TODO
