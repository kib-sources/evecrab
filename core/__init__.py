"""
core/.__init__.py

Ядро системы.

created by pavel in pavel as 10/2/19
Проект evecrab
"""

import datetime

# __author__ = 'pavelmstu'
# __maintainer__ = 'pavelmstu'
# __credits__ = ['pavelmstu', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'


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
