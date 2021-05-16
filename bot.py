import logging
from core import get_settings, Message
from telethon import TelegramClient
from core.detector import AlgorithmicFilter
import asyncio


from telegram import (
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    CallbackContext,
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Информирование пользователя о функционале бота"""
    update.message.reply_text(
        """
        Данный бот предназначет для отправки новостей с функцией
        голосования и вывода результатов
        """
    )


def poll(update: Update, context: CallbackContext) -> None:
    """Отправка опроса"""
    questions = [u'\U0001f44d', u'\U0001f44e']
    text = '**Опрос**\nТут должен быть текст.'
    message = context.bot.send_poll(
        update.effective_chat.id,
        text,
        questions,
        is_anonymous=False,
        allows_multiple_answers=False,
    )
    # Сохранение информации об опросе для последующего использования
    payload = {
        message.poll.id: {
            "options": {question: 0 for question in questions},
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "all_answers": 0,
            "text": text
        }
    }
    context.bot_data.update(payload)


def receive_poll_answer(update: Update, context: CallbackContext) -> None:
    """Обновление статистики опроса"""
    answer_num = update.poll_answer.option_ids[0]
    poll_id = update.poll_answer.poll_id
    questions = context.bot_data[poll_id]["questions"]

    context.bot_data[poll_id]["all_answers"] += 1
    context.bot_data[poll_id]["options"][questions[answer_num]] += 1


def results(update: Update, context: CallbackContext) -> None:
    """Получение результата опросов"""
    poll_ids = list(context.bot_data.keys())
    chat_id = get_settings()['chat_id_to_send_polls_results']

    for poll_id in poll_ids:
        text = context.bot_data[poll_id]['text']
        result = ''
        result += f"<b>Исходный текст</b>:\n" + text + '\n\n'
        result += f"<i>Результаты голосования:</i>\n\nВсего <b>{context.bot_data[poll_id]['all_answers']}</b> голос(a)(ов)\n\n"
        for k, v in context.bot_data[poll_id]['options'].items():
            result += '\t• ' + k + ' - ' + str(v) + '\n\n'
        context.bot.send_message(
            chat_id,
            result,
            parse_mode=ParseMode.HTML,
        )


def preview(update: Update, context: CallbackContext) -> None:
    """Просим пользователя создать опрос и отобразить его предварительный просмотр"""
    try:
        button = [[KeyboardButton("Нажми для создания опроса!", request_poll=KeyboardButtonPollType())]]
        message = "Нажмите кнопку, чтобы бот сгенерировал предварительный просмотр вашего опроса"
        update.effective_message.reply_text(
            message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
        )
    except:
        message = "Опрос можно запросить только в приватных чатах"
        update.effective_message.reply_text(message)


def help_handler(update: Update, context: CallbackContext) -> None:
    """Показывает подсказку"""

    update.message.reply_text("""
        - Выберите /startcrawler для отправки новостей с опросами
    - Выберите /stopcrawler для принудительной остановки краулера
    - Выберите /results для отправки результатов опросов
    """)


async def start_crawler(update: Update, context: CallbackContext) -> None:
    # Список каналов
    channel_list = get_settings()['telegram_chat_links_list']

    # Чат, в который мы будем отправлять сообщение
    # CHAT_ID = get_settings()['chat_to_send_events_id']
    chat_id = get_settings()['chat_id_to_send_polls']

    # Получаем необходимые настройки
    settings = get_settings()

    questions = [u'\U0001f44d', u'\U0001f44e']

    async with TelegramClient(settings['username'], settings['api_id'], settings['api_hash']) as client:

        for chanel in channel_list[:1]:

            async for message in client.iter_messages(chanel, limit=10):

                message = Message(chanel, message.text, datetime_=message.date)
                # Инициализация детектора и передача текста детектору
                detector = AlgorithmicFilter(message)
                # Определение текста на начиличие заданных тем
                is_IS_event = detector.detect_event(True) and detector.detect_is(True)

                if is_IS_event:

                    context.bot.send_message(
                        chat_id,
                        detector.message.description,
                        parse_mode=ParseMode.HTML,
                    )

                    message_to_send = context.bot.send_poll(
                        # update.effective_chat.id,
                        chat_id,
                        'Как тебе новость?',
                        questions,
                        is_anonymous=False,
                        allows_multiple_answers=False,
                    )

                    # Сохранение информации об опросе для последующего использования
                    payload = {
                        message_to_send.poll.id: {
                            "options": {question: 0 for question in questions},
                            "questions": questions,
                            "message_id": message_to_send.message_id,
                            "chat_id": update.effective_chat.id,
                            "all_answers": 0,
                            "text": detector.message.description + '\n#ID: ' + str(message_to_send.message_id)
                        }
                    }

                    context.bot_data.update(payload)


loop = asyncio.new_event_loop()


def start_crawler_run(update: Update, context: CallbackContext):
    loop.run_until_complete(start_crawler(update, context))


def stop_crawler(update: Update, context: CallbackContext):
    loop.close()


def main():
    # Создаем экземпляр Updater и передаем токен бота.
    updater = Updater(get_settings()['bot_token'])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(CommandHandler('poll', poll))
    dispatcher.add_handler(CommandHandler('results', results))
    dispatcher.add_handler(CommandHandler('startcrawler', start_crawler_run))
    dispatcher.add_handler(CommandHandler('stopcrawler', stop_crawler))
    dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))
    # dispatcher.add_handler(CommandHandler('preview', preview))
    dispatcher.add_handler(CommandHandler('help', help_handler))

    # Старт бота
    updater.start_polling()

    # Запускаем бота до тех пор, пока пользователь не нажмет Ctrl-C или процесс не получит SIGINT
    # SIGTERM или SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()