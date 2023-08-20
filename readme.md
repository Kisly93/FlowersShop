# FlowerShop #

## Установка

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

## Запуск
- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте файл базы данных и сразу примените все миграции командой `python3 manage.py migrate`
- Для создания пользователя админ-панели `python3 manage.py createsuperuser`
- Запустите сервер командой `python3 manage.py runserver`

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны переменные:
- `TELEGRAM_TOKEN` - токен телеграм бота
- `TELEGRAM_OWNER_ID` - id получателя уведомлений

- `SECRET_KEY` - секретный ключ проекта (обязательно)
- `STRIPE_API_KEY` - API-ключ, полученный из системы STRIPE.

- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).

Прочие переменные(достаточно скопировать):

SECURE_HSTS_SECONDS=10
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
SECURE_HSTS_PRELOAD=True
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_SSL_REDIRECT=True



