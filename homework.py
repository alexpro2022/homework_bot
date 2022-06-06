import logging
import os
import sys
import time


import requests
import telegram

from dotenv import load_dotenv

load_dotenv()

GLOBAL_VARIABLES_NAMES = (
    'PRACTICUM_TOKEN',
    'TELEGRAM_TOKEN',
    'TELEGRAM_CHAT_ID'
)
PRACTICUM_TOKEN = os.getenv(GLOBAL_VARIABLES_NAMES[0])
TELEGRAM_TOKEN = os.getenv(GLOBAL_VARIABLES_NAMES[1])
TELEGRAM_CHAT_ID = os.getenv(GLOBAL_VARIABLES_NAMES[2])

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

SYSTEM_EXIT_PHRASE = 'Программа принудительно остановлена.'
STATUS_NOTHING_PHRASE = 'Отсутствие в ответе новых статусов.'
CHECK_TOKENS_PHRASE = (
    'Отсутствует обязательная переменная окружения: {name}.')
PARSE_STATUS_RETURN_PHRASE = (
    'Изменился статус проверки работы "{name}". {verdict}')
PARSE_STATUS_ERROR_PHRASE = (
    'Неожиданный статус домашней работы в ответе API: {status}.')
SEND_MESSAGE_INFO_PHRASE = 'Telegram-Бот отправил сообщение: {message}.'
SEND_MESSAGE_EXCEPT_PHRASE = 'Cбой при отправке Telegram-сообщения: {message}.'
HTTP_ERROR_PHRASE = 'Http статус: {status_code}, {message}.'
CONNECTION_ERROR_PHRASE = 'Ошибка соединения: {message}.'
TIMEOUT_ERROR_PHRASE = 'Время ожидания истекло: {message}.'
REQUEST_ERROR_PHRASE = 'Ошибка запроса к серверу: {message}.'
RESPONSE_IS_NOT_DICT_PHRASE = 'Ответ от API не в виде словаря.'
KEY_IS_NOT_IN_RESPONSE_PHRASE = (
    'Отсутствие ключа "homeworks" в ответе API.')
HOMEWORKS_IS_NOT_LIST_PHRASE = 'Ответ от API не в виде списка.'


def check_tokens():
    """Проверяет доступность переменных окружения для работы программы."""
    if all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)):
        return True
    for name in GLOBAL_VARIABLES_NAMES:
        if not globals()[name]:
            logging.critical(CHECK_TOKENS_PHRASE.format(name=name))
    return False


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info(SEND_MESSAGE_INFO_PHRASE.format(message=message))
        return True
    except telegram.TelegramError:
        logging.exception(SEND_MESSAGE_EXCEPT_PHRASE.format(message=message))
        return False


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    params = {'from_date': current_timestamp}
    message = f'for URL: {ENDPOINT}, Headers: {HEADERS}, params: {params}: '
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.exceptions.ConnectionError as errc:
        raise requests.exceptions.ConnectionError(
            CONNECTION_ERROR_PHRASE.format(message=message)) from errc
    except requests.exceptions.Timeout as errt:
        raise requests.exceptions.Timeout(
            TIMEOUT_ERROR_PHRASE.format(message=message)) from errt
    except requests.exceptions.RequestException as err:
        raise requests.exceptions.RequestException(
            REQUEST_ERROR_PHRASE.format(message=message)) from err
    if isinstance(response.status_code, int) and response.status_code != 200:
        raise requests.exceptions.HTTPError(
            HTTP_ERROR_PHRASE.format(
                status_code=response.status_code, message=message))
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность.
    В качестве параметра функция получает ответ API, приведенный
    к типам данных Python. Если ответ API соответствует ожиданиям,
    то функция должна вернуть список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'.
    """
    if not isinstance(response, dict):
        raise TypeError(RESPONSE_IS_NOT_DICT_PHRASE)
    if 'homeworks' not in response:
        raise KeyError(KEY_IS_NOT_IN_RESPONSE_PHRASE)
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError(HOMEWORKS_IS_NOT_LIST_PHRASE)
    return homeworks


def parse_status(homework):
    """Извлекает статус из информации о конкретной домашней работе."""
    name = homework['homework_name']
    status = homework['status']
    try:
        verdict = HOMEWORK_VERDICTS[status]
    except KeyError as error:
        raise KeyError(
            PARSE_STATUS_ERROR_PHRASE.format(status=status)
        ) from error
    return PARSE_STATUS_RETURN_PHRASE.format(name=name, verdict=verdict)


def set_log():
    """Устанавливает настройки логирования."""
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s, %(levelname)s, %(name)s, '
            '%(funcName)s, %(lineno)s, %(message)s'
        ),
        handlers=[
            logging.FileHandler(
                __file__.split('.')[0] + '.log',
                encoding='utf-8'
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """
    Основная логика работы бота.
    Сделать запрос к API. Проверить ответ. Если есть обновления —
    получить статус работы из обновления и отправить сообщение в Telegram.
    Подождать некоторое время и сделать новый запрос.
    """
    set_log()
    if not check_tokens():
        raise SystemExit(SYSTEM_EXIT_PHRASE)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)

    current_timestamp = int(time.time())
    prev_message = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            current_timestamp = response.get('current_date', current_timestamp)
            homeworks = check_response(response)
            if not homeworks:
                logging.debug(STATUS_NOTHING_PHRASE)
            else:
                send_message(bot, parse_status(homeworks[0]))
        except Exception as error:
            message = f'{error}'
            logging.exception(message)
            if message != prev_message:
                if send_message(bot, message):
                    prev_message = message
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
