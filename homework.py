import logging
import os
import requests
import sys
import telegram
import time

from dotenv import load_dotenv


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s, %(levelname)s, %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(name)s, %(levelname)s, %(message)s'
)
handler.setFormatter(formatter)


def check_tokens():
    """Проверяет доступность переменных окружения для работы программы."""
    missing_var = 'PRACTICUM_TOKEN'
    if PRACTICUM_TOKEN:
        if TELEGRAM_TOKEN:
            if TELEGRAM_CHAT_ID:
                return True
            else:
                missing_var = 'TELEGRAM_CHAT_ID'
        else:
            missing_var = 'TELEGRAM_TOKEN'
    logger.critical(
        f'Отсутствует обязательная переменная окружения: "{missing_var}".'
        f'Программа принудительно остановлена.'
    )
    return False


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception:
        logger.exception('Cбой при отправке сообщения в Telegram')
    else:
        logger.info(f'Бот отправил сообщение в Telegram: {message}')


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        raise Exception(
            f'Недоступность эндпоинта Практикума - ошибка: {error}'
        )
    if response.status_code != 200:
        raise Exception(f'HTTP status code {response.status_code}')
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность.
    В качестве параметра функция получает ответ API, приведенный
    к типам данных Python. Если ответ API соответствует ожиданиям,
    то функция должна вернуть список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'.
    """
    for key in ('homeworks', 'current_date'):
        try:
            response[key]
        except KeyError as error:
            raise Exception(
                f'Отсутствие ожидаемого ключа ["{key}"] в ответе API: {error}'
            )
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise Exception('Ответ от API не в виде списка')
    return homeworks


def parse_status(homework):
    """Извлекает статус из информации о конкретной домашней работе."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except KeyError:
        raise Exception(
            f'Недокументированный статус домашней работы'
            f'в ответе API: {homework_status}')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """
    Основная логика работы бота.
    Сделать запрос к API. Проверить ответ. Если есть обновления —
    получить статус работы из обновления и отправить сообщение в Telegram.
    Подождать некоторое время и сделать новый запрос.
    """
    if not check_tokens():
        raise Exception(
            'Отсутствует обязательная переменная окружения.'
            'Программа принудительно остановлена.'
        )

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    current_timestamp = int(time.time())
    prev_message = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            current_timestamp = response['current_date']
            if not homeworks:
                logger.debug('Отсутствие в ответе новых статусов.')
            else:
                for homework in homeworks:
                    send_message(bot, parse_status(homework))
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.exception(message)
            if message != prev_message:
                send_message(bot, message)
                prev_message = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
