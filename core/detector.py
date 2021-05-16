"""
core.detector базовый модуль ЭС, обнаруживающая полезную информацию в тексте
"""
import numpy as np
import re
from pymystem3 import Mystem
import core


class BaseFilter:
    """
    Базовый фильтр событий определенной тематики
    """

    def __init__(self, message):
        self.message = message

    def detect_is(self):
        ...

    def detect_event(self):
        ...

    def convert_text(self, text):
        """
        Функция, преобразующая текст перед анализом
        :param text: String
        :return: String
        """
        # Удаляем эмодзи
        regex_pattern = re.compile(pattern="["
                                           u"\U0001F600-\U0001F64F"  # эмоции
                                           u"\U0001F300-\U0001F5FF"  # символы и пиктограммы
                                           u"\U0001F680-\U0001F6FF"  # символы транспорта и карты
                                           u"\U0001F1E0-\U0001F1FF"  # флаги (iOS)
                                           "]+", flags=re.UNICODE)
        text = regex_pattern.sub(r'', text.replace('✔️', ''))
        text = text.replace('\n', ' ').replace('\t', ' ').lower()
        # Преобразуем все ссылки в токен link
        text = re.sub(r'\[(.+)\]\(\S+\)', r'\g<1> link', text)
        text = re.sub(r'https?:\/\/(www\.)?([a-zA-Z0-9\.]){1,256}(\/[\-\w\d]+){0,20}(\.[\w]{1,20})?(\?[\w\d=]+)?',
                      'link', text)
        return text


class AlgorithmicFilter(BaseFilter):
    """
    Фильтр, детектирующий тексты на основе жесткого алгоритма
    """

    def __init__(self, message):
        super().__init__(message)

        # Словарь слов про ИБ
        self.DETECT_IS_SET = core.get_is_set()

        # Словарь слов про события
        self.DETECT_EVENT_SET = core.get_events_set()

    def detect_is(self, add_detected_word=False):
        """
        Метод, определяющий, есть ли в переданном сообщении информация про ИБ
        :param add_detected_word: bool, default=False
            Добавлять ли в начало сообщения слово, по которому была детектирована тема ИБ
        :return: bool
        """

        # Флаг, определяющий, содержит ли данный текст информацию про ИБ
        is_IS = False

        # Слово, по которому сработал алгоритм
        detected_word = ''

        # Инициализация лемматизатора
        lemmatizer = Mystem(grammar_info=False, entire_input=False)

        # Перебор всех слов
        for norm_word in lemmatizer.lemmatize(self.convert_text(self.message.description)):

            # Есть ли данное слово в словаре слов про ИБ
            if norm_word in self.DETECT_IS_SET:
                is_IS = True
                detected_word = norm_word
                break

        if add_detected_word:
            self.message.description = '#' + detected_word + '\n' + self.message.description

        return is_IS

    def detect_event(self, add_detected_word=False):
        """
        Метод, определяющий, есть ли в переданном сообщении информация про событие
        :param add_detected_word: bool, default=False
            Добавлять ли в начало сообщения слово, по которому было детектировано событие
            :return: bool
        """

        # Флаг, определяющий, содержит ли данный текст информацию про событие
        is_event = False

        # Слово, по которому сработал алгоритм
        detected_word = ''

        # Инициализация лемматизатора
        lemmatizer = Mystem(grammar_info=False, entire_input=False)

        # Перебор всех слов
        for norm_word in lemmatizer.lemmatize(self.convert_text(self.message.description)):

            # Есть ли данное слово в словаре слов про ИБ
            if norm_word in self.DETECT_EVENT_SET:
                is_event = True
                detected_word = norm_word
                break

        if add_detected_word:
            self.message.description = '#' + detected_word + '\n' + self.message.description

        return is_event


