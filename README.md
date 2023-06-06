# Проект: Telegram Bot
[![status](https://github.com/alexpro2022/homework_bot/actions/workflows/main.yml/badge.svg)](https://github.com/alexpro2022/homework_bot/actions)
[![codecov](https://codecov.io/gh/alexpro2022/homework_bot/branch/master/graph/badge.svg?token=VJVG3LCS7A)](https://codecov.io/gh/alexpro2022/homework_bot)

В этом приложении реализован Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.


## Оглавление:
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Создание и настройка аккаунта бота](#создание-и-настройка-аккаунта-бота)
- [Установка и запуск](#установка-и-запуск)
- [Удаление](#удаление)
- [Автор](#автор)



## Технологии:
<details><summary>Развернуть</summary>

**Языки программирования, библиотеки и модули:**

[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/-python--telegram--bot-464646?logo=Python)](https://docs.python-telegram-bot.org/en/stable/index.html) 
[![logging](https://img.shields.io/badge/-logging-464646?logo=python)](https://docs.python.org/3/library/logging.html)
[![os](https://img.shields.io/badge/-os-464646?logo=python)](https://docs.python.org/3/library/os.html)
[![sys](https://img.shields.io/badge/-sys-464646?logo=python)](https://docs.python.org/3/library/sys.html)
[![time](https://img.shields.io/badge/-time-464646?logo=python)](https://docs.python.org/3/library/time.html)
[![python-dotenv](https://img.shields.io/badge/-python--dotenv-464646?logo=Python)](https://pypi.org/project/python-dotenv/)
[![Requests](https://img.shields.io/badge/-Requests:_HTTP_for_Humans™-464646?logo=Python)](https://pypi.org/project/requests/)


**Тестирование:**

[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-cov](https://img.shields.io/badge/-Pytest--cov-464646?logo=Pytest)](https://pytest-cov.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/badge/-Coverage-464646?logo=Python)](https://coverage.readthedocs.io/en/latest/)


**CI/CD:**

[![GitHub_Actions](https://img.shields.io/badge/-GitHub_Actions-464646?logo=GitHub)](https://docs.github.com/en/actions)
[![docker_hub](https://img.shields.io/badge/-Docker_Hub-464646?logo=docker)](https://hub.docker.com/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/) 
[![Telegram](https://img.shields.io/badge/-Telegram-464646?logo=Telegram)](https://core.telegram.org/api)

[⬆️Оглавление](#оглавление)
</details>


## Описание работы:
Что умеет делать бот:
  * раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
  * при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
  * логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

Краткая документация к API-сервису и примеры запросов доступны в шпаргалке «API сервиса Практикум.Домашка»:
https://code.s3.yandex.net/backend-developer/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC.%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BA%D0%B0%20%D0%A8%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0.pdf

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


## Установка и запуск:
Удобно использовать принцип copy-paste - копировать команды из GitHub Readme и вставлять в командную строку Git Bash или IDE (например VSCode).
### Предварительные условия для Docker:
<details><summary>Развернуть</summary>

Предполагается, что пользователь:
 - создал [бота](#создание-и-настройка-аккаунта-бота).
 - создал аккаунт [DockerHub](https://hub.docker.com/), если запуск будет производиться на удаленном сервере.
 - установил [Docker](https://docs.docker.com/engine/install/) на удаленном сервере. Проверить наличие можно выполнив команду:
    ```bash
    docker --version
    ```
</details>
<h2></h2>
<details><summary>Локальный запуск</summary>

1. Клонируйте репозиторий с GitHub: 
```bash
git clone https://github.com/alexpro2022/homework_bot.git && \
cd homework_bot && \
cp env_example .env && \
nano .env
```

2. В открывшемся новом **.env**-файле введите данные для переменных окружения:
```bash
PRACTICUM_TOKEN=
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
```

  - Получить PRACTICUM_TOKEN можно по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a
  - Получить токен вашего бота можно у бота @BotFather командой /mybots и далее API Token.
  - Узнать свой ID можно у бота @userinfobot.

Если у вас нет аккаунта бота в Телеграм, его надо [создать](#создание-и-настройка-аккаунта-бота)

3. Создайте и активируйте виртуальное окружение:
   * Если у вас Linux/macOS
   ```bash
    python -m venv venv && source venv/bin/activate
   ```
   * Если у вас Windows
   ```bash
    python -m venv venv && source venv/Scripts/activate
   ```

4. Установите в виртуальное окружение все необходимые зависимости из файла **requirements.txt**:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```

5. Для запуска выполните команду:

```bash
python homework.py
```
 
6. Остановить приложение можно комбинацией клавиш Ctl-C. 
 
 <h2></h2>
</details>

<details><summary>Запуск на удаленном сервере</summary> 

1. Сделайте [форк](https://docs.github.com/en/get-started/quickstart/fork-a-repo) в свой репозиторий.

2. Создайте `Actions.Secrets` согласно списку ниже:
```py
# переменные окружения из env_example файла:
PRACTICUM_TOKEN=
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
 
PROJECT_NAME

DOCKERHUB_USERNAME
DOCKERHUB_PASSWORD

# Данные удаленного сервера и ssh-подключения:
HOST  # публичный IP-адрес вашего удаленного сервера
USERNAME
SSH_KEY  
PASSPHRASE
```

3. Запустите вручную `workflow`, чтобы автоматически развернуть проект в docker-контейнере на удаленном сервере.
</details>
<h2></h2>
 
[⬆️Оглавление](#оглавление)


## Удаление:
Для удаления проекта выполните команду:
```bash
cd .. && rm -fr homework_bot && deactivate
```
  
[⬆️Оглавление](#оглавление)


## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#Проект-Telegram-Bot)
