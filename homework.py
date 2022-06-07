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
MISSING_TOKENS_PHRASE = (
    'Отсутствует обязательная переменная окружения: {name}.')
PARSE_STATUS_RETURN_PHRASE = (
    'Изменился статус проверки работы "{name}". {verdict}')
PARSE_STATUS_ERROR_PHRASE = (
    'Неожиданный статус домашней работы в ответе API: {status}.')
PRAKTIKUM_ATTRIBUTES = f'URL: {ENDPOINT}, Headers: {HEADERS} '
PRAKTIKUM_INVALID_TOKEN = (
    f'Проблема аутентификации, возможная причина - '
    f'неверный токен Практикума. {SYSTEM_EXIT_PHRASE}')
TELEGRAM_INFO = 'Telegram-Бот отправил сообщение: {message}.'
TELEGRAM_BAD_REQUEST = (
    'Telegram не может обработать запрос => '
    'Возможные причины - неверный chat_id => '
    'сбой при отправке Telegram-сообщения => {message}.')
TELEGRAM_INVALID_TOKEN = (
    f'Неверный Telegram токен => '
    f'Невозможно активировать Бот => {SYSTEM_EXIT_PHRASE}')
TELEGRAM_TIME_OUT = (
    'Время запроса истекло => '
    'сбой при отправке Telegram-сообщения => {message}.')
TELEGRAM_UNAUTHORIZED = (
    'У Бота не достаточно прав чтобы выполнить требуемое действие => '
    'сбой при отправке Telegram-сообщения => {message}.')
TELEGRAM_NETWORK_ERROR = (
    'Проблемы с сетью => '
    'сбой при отправке Telegram-сообщения => {message}.')
TELEGRAM_ERROR = (
    'Проблемы с Telegram => '
    'сбой при отправке Telegram-сообщения => {message}.')
HTTP_ERROR_PHRASE = 'Http статус: {status_code}.'
REQUEST_ERROR_PHRASE = f'Ошибка запроса к серверу: {PRAKTIKUM_ATTRIBUTES}.'
RESPONSE_IS_NOT_DICT_PHRASE = (
    'Ответ API "JSON" не удалось преобразован в словарь.')
KEY_IS_NOT_IN_RESPONSE_PHRASE = 'Отсутствие ключа ["homeworks"] в ответе API.'
HOMEWORKS_IS_NOT_LIST_PHRASE = (
    'Ответ API не содержит список под ключом ["homeworks"].')
SERVER_ERROR_PHRASE = 'Сбой Сервера с ошибками: {server_errors}'
MAIN_ERROR_PHRASE = 'Сбой в программе: {error}'


class TokenError(Exception):
    """Исключение для невалидного токена Практикума."""

    pass


class ServerError(Exception):
    """Исключение для ошибок сервера Практикума."""

    pass


def check_tokens():
    """Проверяет доступность переменных окружения для работы программы."""
    ok = True
    for name in GLOBAL_VARIABLES_NAMES:
        if not globals()[name]:
            logging.critical(MISSING_TOKENS_PHRASE.format(name=name))
            if ok:
                ok = False
    return ok


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params={
            'from_date': current_timestamp})
    except requests.exceptions.RequestException as err:
        raise ServerError(
            f'{current_timestamp} sec: {REQUEST_ERROR_PHRASE} {err}') from err
    if response.status_code == 401:
        raise TokenError(PRAKTIKUM_INVALID_TOKEN)
    if response.status_code != 200:
        raise ServerError(
            f'{current_timestamp} sec: ',
            HTTP_ERROR_PHRASE.format(status_code=response.status_code))
    response_json = response.json()
    server_errors = []
    for item in ('code', 'error'):
        if item in response_json:
            server_errors.append(f'{item} : {response_json[item]}')
    if server_errors:
        raise ServerError(
            SERVER_ERROR_PHRASE.format(server_errors=server_errors))
    return response_json


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


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info(TELEGRAM_INFO.format(message=message))
        return True
    except telegram.error.BadRequest:
        logging.exception(TELEGRAM_BAD_REQUEST.format(message=message))
    except telegram.error.TimedOut:
        logging.exception(TELEGRAM_TIME_OUT.format(message=message))
    except telegram.error.Unauthorized:
        logging.exception(TELEGRAM_UNAUTHORIZED.format(message=message))
    except telegram.error.NetworkError:
        logging.exception(TELEGRAM_NETWORK_ERROR.format(message=message))
    except telegram.error.TelegramError:
        logging.exception(TELEGRAM_ERROR.format(message=message))
    return False


def main():
    """
    Основная логика работы бота.
    Сделать запрос к API. Проверить ответ. Если есть обновления —
    получить статус работы из обновления и отправить сообщение в Telegram.
    Подождать некоторое время и сделать новый запрос.
    """
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
    except telegram.error.InvalidToken:
        logging.exception(TELEGRAM_INVALID_TOKEN)
        return
    current_timestamp = int(time.time())
    prev_error, prev_status = '', ''
    while True:
        try:
            response_json = get_api_answer(current_timestamp)
            homeworks = check_response(response_json)
            if homeworks:
                status = parse_status(homeworks[0])
            else:
                status = STATUS_NOTHING_PHRASE
            if status != prev_status:
                if status == STATUS_NOTHING_PHRASE:
                    logging.info(status)
                    prev_status = status
                elif send_message(bot, status):
                    prev_status = status
                    current_timestamp = response_json.get(
                        'current_date', current_timestamp)
        except Exception as exc_error:
            error = MAIN_ERROR_PHRASE.format(error=exc_error)
            logging.exception(error)
            if prev_error != error and send_message(bot, error):
                prev_error = error
            if isinstance(exc_error, TokenError):
                return
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
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
    if check_tokens():
        main()
    else:
        logging.critical(SYSTEM_EXIT_PHRASE)
