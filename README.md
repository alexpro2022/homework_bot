# Проект: Telegram Bot
[![status](https://github.com/alexpro2022/homework_bot/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/homework_bot/actions)
[![codecov](https://codecov.io/gh/alexpro2022/homework_bot/branch/master/graph/badge.svg?token=VJVG3LCS7A)](https://codecov.io/gh/alexpro2022/homework_bot)
В этом приложении реализован Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнавать статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.


## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка](#установка)
- [Запуск](#запуск)
- [Автор](#автор)



## Технологии:
<!-- 1. Языки программирования, библиотеки и пакеты: -->
[![Python](https://warehouse-camo.ingress.cmh1.psfhosted.org/7c5873f1e0f4375465dfebd35bf18f678c74d717/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7072657474797461626c652e7376673f6c6f676f3d707974686f6e266c6f676f436f6c6f723d464645383733)](https://www.python.org/)
[![PTB](https://img.shields.io/badge/-Python_Telegram_Bot-464646?logo=Python)](https://docs.python-telegram-bot.org/en/stable/index.html)
[![Requests](https://img.shields.io/badge/-Requests:_HTTP_for_Humans™-464646?logo=Python)](https://pypi.org/project/requests/)

<!-- 2. Тесты: -->
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)
<!-- 3. Фреймворки, библиотеки и пакеты: -->
<!-- 4. Базы данных: -->
<!-- 5. CI/CD: -->
[![GitHub](https://img.shields.io/badge/-GitHub-464646?logo=GitHub)](https://docs.github.com/en)
[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)

[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)



## Описание работы:
Краткая документация к API-сервису и примеры запросов доступны в шпаргалке «API сервиса Практикум.Домашка».

[⬆️Оглавление](#оглавление)



## Установка:
1. Клонировать репозиторий с GitHub:
```
git clone git@github.com:alexpro2022/homework_bot.git
```

2. Перейти в созданную директорию проекта:
```
cd homework_bot
```

3. Создать и активировать виртуальное окружение:
```
python -m venv venv
```
* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

4. Установить все необходимые зависимости из файла **requirements.txt**:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
pip list
```

5. Скопируйте содержимое файла **env_example** (при этом будет создан файл *.env*):
```
cp env_example .env
```

6. Откройте новый **.env**-файл и введите данные для переменных окружения:
    PRACTICUM_TOKEN=
    TELEGRAM_TOKEN=
    TELEGRAM_CHAT_ID=

  - Получить PRACTICUM_TOKEN можно по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.
  - Получить токен вашего бота можно у бота @BotFather.
  - Узнать свой ID можно у бота @userinfobot.


[⬆️Оглавление](#оглавление)



## Запуск:

Выполните команду:

```
python homework.py
```

[⬆️Оглавление](#оглавление)



## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#Проект-Telegram-Bot)
