"""
worker -- запускаемый воркер

created by pavel in pavel as 10/2/19
Проект evecrab
"""
from time import sleep
import datetime

from core.telega import send_message

# TODO пишите все краулеры в модуле crawlers
# from crawlers. ... import ...

__author__ = 'pavelmstu'
__maintainer__ = 'pavelmstu'
__credits__ = ['pavelmstu', ]
__copyright__ = "КИБ"
__status__ = 'Development'
__version__ = '20191002'


CYCLE_SLEEP_TIME = 60

# Список краулеров
CRAWLER_LIST = [
    # TODO напишите и укажите здесь все краулеры
]


def one_cycle():
    for crawler in CRAWLER_LIST:
        for message in crawler:
            send_message(message)


def main():
    print(datetime.datetime.now())

    while True:
        one_cycle()
        sleep(CYCLE_SLEEP_TIME)


if __name__ == "__main__":
    main()
