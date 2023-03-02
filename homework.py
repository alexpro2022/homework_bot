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

SYSTEM_EXIT = 'Программа принудительно остановлена.'
STATUS_NOTHING = 'Отсутствие в ответе новых статусов.'
MISSING_TOKENS = (
    'Отсутствует обязательная переменная окружения: {name}.')
PARSE_STATUS_RETURN = (
    'Изменился статус проверки работы "{name}". {verdict}')
PARSE_STATUS_ERROR = (
    'Неожиданный статус домашней работы в ответе API: {status}.')
TELEGRAM_BOT_ACTIVATION_FAILED = (
    'Невозможно активировать Бот. Ошибка => {error}. '
    'Передача сообщений в Telegram отключена.')
TELEGRAM_INFO = 'Telegram-Бот отправил сообщение:\n"{message}"'
TELEGRAM_ERROR = (
    'Сбой отправки Telegram-сообщения:\n"{message}"\n'
    'Ошибка => {error}\n'
    'Чат № {chat_id}')
HTTP_ERROR = (
    'Http статус: {status_code}.\nПараметры запроса => '
    'URL: {url}, Заголовки: {headers}, Время: {params} сек.')
REQUEST_ERROR = (
    'Ошибка запроса к серверу.\nПараметры запроса => '
    'URL: {url}, Заголовки: {headers}, Время: {params} сек.')
SERVER_ERROR = (
    'Сбой Сервера с ошибками: {server_errors}.\nПараметры запроса => '
    'URL: {url}, Заголовки: {headers}, Время: {params} сек.')
KEY_IS_NOT_IN_RESPONSE = 'Отсутствие ключа ["homeworks"] в ответе API.'
RESPONSE_IS_NOT_DICT = (
    'Ответ API "JSON" не удалось преобразован в словарь.\n'
    'Тип ответа: {tipe}')
HOMEWORKS_IS_NOT_LIST = (
    'Ответ API не содержит список под ключом ["homeworks"].\n'
    'Тип ответа: {tipe}')
MAIN_ERROR = 'Сбой в программе. Ошибка => {error}'


class ServerError(Exception):
    """Исключение для ошибок сервера Практикума."""


def check_tokens():
    """Проверяет доступность переменных окружения для работы программы."""
    ok = True
    for name in GLOBAL_VARIABLES_NAMES:
        if not globals()[name]:
            logging.critical(MISSING_TOKENS.format(name=name))
            ok = False
    return ok


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    params = {'from_date': current_timestamp}
    req_params = dict(url=ENDPOINT, headers=HEADERS, params=params)
    try:
        response = requests.get(**req_params)
    except requests.exceptions.RequestException as err:
        raise ConnectionError(REQUEST_ERROR.format(**req_params)) from err
    if response.status_code != 200:
        raise ServerError(
            HTTP_ERROR.format(status_code=response.status_code, **req_params))
    response_json = response.json()
    server_errors = []
    for item in ('code', 'error'):
        if item in response_json:
            server_errors.append(f'{item} : {response_json[item]}')
    if server_errors:
        raise ServerError(
            SERVER_ERROR.format(
                server_errors=server_errors, **req_params))
    return response_json


def check_response(response):
    """Проверяет ответ API на корректность.
    В качестве параметра функция получает ответ API, приведенный
    к типам данных Python. Если ответ API соответствует ожиданиям,
    то функция должна вернуть список домашних работ (он может быть и пустым),
    доступный в ответе API по ключу 'homeworks'.
    """
    if not isinstance(response, dict):
        raise TypeError(RESPONSE_IS_NOT_DICT.format(tipe=type(response)))
    if 'homeworks' not in response:
        raise KeyError(KEY_IS_NOT_IN_RESPONSE)
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError(HOMEWORKS_IS_NOT_LIST.format(tipe=type(homeworks)))
    return homeworks


def parse_status(homework):
    """Извлекает статус из информации о конкретной домашней работе."""
    name = homework['homework_name']
    status = homework['status']
    try:
        verdict = HOMEWORK_VERDICTS[status]
    except KeyError:
        raise ValueError(PARSE_STATUS_ERROR.format(status=status))
    return PARSE_STATUS_RETURN.format(name=name, verdict=verdict)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info(TELEGRAM_INFO.format(message=message))
        return True
    except telegram.error.TelegramError as error:
        logging.exception(TELEGRAM_ERROR.format(
            chat_id=TELEGRAM_CHAT_ID, message=message, error=error))
        return False


def main():
    """
    Основная логика работы бота.
    Сделать запрос к API. Проверить ответ. Если есть обновления —
    получить статус работы из обновления и отправить сообщение в Telegram.
    Подождать некоторое время и сделать новый запрос.
    """
    if not check_tokens():
        logging.critical(SYSTEM_EXIT)
        return
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
    except telegram.error.TelegramError as error:
        logging.exception(TELEGRAM_BOT_ACTIVATION_FAILED.format(error=error))
        return
    current_timestamp = int(time.time())
    prev_error = ''
    while True:
        try:
            response_json = get_api_answer(current_timestamp)
            homeworks = check_response(response_json)
            if homeworks:
                if send_message(bot, parse_status(homeworks[0])):
                    current_timestamp = response_json.get(
                        'current_date', current_timestamp)
            else:
                logging.debug(STATUS_NOTHING)
        except Exception as exc_error:
            error = MAIN_ERROR.format(error=exc_error)
            logging.exception(error)
            if prev_error != error and send_message(bot, error):
                prev_error = error
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s : %(levelname)s, %(name)s, '
            '%(funcName)s, %(lineno)s, %(message)s'),
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                f'{__file__}.log',
                encoding='utf-8')
        ])
    main()
