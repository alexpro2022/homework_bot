# Проект: Telegram Bot
[![status](https://github.com/alexpro2022/homework_bot/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/homework_bot/actions)
[![codecov](https://codecov.io/gh/alexpro2022/homework_bot/branch/master/graph/badge.svg?token=VJVG3LCS7A)](https://codecov.io/gh/alexpro2022/homework_bot)

В этом приложении реализован Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.


## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка](#установка)
- [Создание и настройка аккаунта бота](#Создание%20и%20настройка%20аккаунта%20бота)
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
Что умеет делать бот:
  * раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
  * при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
  * логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

Краткая документация к API-сервису и примеры запросов доступны в шпаргалке «API сервиса Практикум.Домашка»:
https://code.s3.yandex.net/backend-developer/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC.%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BA%D0%B0%20%D0%A8%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0.pdf

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
    ```
    PRACTICUM_TOKEN=
    TELEGRAM_TOKEN=
    TELEGRAM_CHAT_ID=
    ```

  - Получить PRACTICUM_TOKEN можно по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a
  - Получить токен вашего бота можно у бота @BotFather командой /mybots и далее API Token.
  - Узнать свой ID можно у бота @userinfobot.

Если у вас нет аккаунта бота в Телеграм, его надо создать [Создание и настройка аккаунта бота](#Создание%20и%20настройка%20аккаунта%20бота)

[⬆️Оглавление](#оглавление)



## Создание и настройка аккаунта бота:
1. @BotFather — регистрирует аккаунты ботов в Telegram:

Найдите в Telegram бота @BotFather: в окно поиска над списком контактов введите его имя.
Обратите внимание на иконку возле имени бота: белая галочка на голубом фоне. Эту иконку устанавливают администраторы Telegram, она означает, что бот настоящий, а не просто носит похожее имя. В любой непонятной ситуации выполняйте команду /help — и @BotFather покажет вам, на что он способен.

2. Создание аккаунта бота:

Начните диалог с ботом @BotFather: нажмите кнопку Start («Запустить»). Затем отправьте команду /newbot и укажите параметры нового бота:
   * имя (на любом языке), под которым ваш бот будет отображаться в списке контактов;
   * техническое имя вашего бота, по которому его можно будет найти в Telegram. Имя должно оканчиваться на слово bot в любом регистре. Имена ботов должны быть уникальны.

Аккаунт для вашего бота создан! 
@BotFather поздравит вас и отправит в чат токен для работы с Bot API. Токен выглядит примерно так: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11. По вашему запросу @BotFather может отозвать токен (отправьте боту @BotFather команду /revoke) и сгенерировать новый.

3. Настройка аккаунта бота:
Настроить аккаунт бота можно через @BotFather.
Отправьте команду /mybots; в ответ вы получите список ботов, которыми вы управляете (возможно, в этом списке лишь один бот). Укажите бота, которого хотите отредактировать, и нажмите кнопку Edit Bot.
Вы сможете изменить:
   * Имя бота (Edit Name).
   * Описание (Edit Description) — текст, который пользователи увидят в самом начале диалога с ботом под заголовком «Что может делать этот бот?»
   * Общую информацию (Edit About) — текст, который будет виден в профиле бота.
   * Картинку-аватар (Edit Botpic).
   * Команды (Edit Commands) — подсказки для ввода команд.

4. Активация бота:

Найдите своего бота по имени через поисковую строку — точно так же, как вы искали @BotFather. Нажмите кнопку Start («СТАРТ»), чтобы активировать его: теперь он сможет отправлять вам сообщения. Точно так же активировать вашего бота может любой, кто его найдёт.

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
