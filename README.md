# FlowerShop #
Сайт для торговли букетами.

Внешний вид сайта

![FlowersShop-main](https://github.com/Kisly93/FlowersShop/assets/111083714/4b851633-782e-4257-9faf-e4d5b500a821)


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

## Переменные окружения

Скачайте код `git clone https://github.com/[......]/FlowersShop`  

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` 
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Требуемые переменные:
- `TELEGRAM_TOKEN` - токен Вашего бота от Telegram. [Инструкция, как создать бота.](https://core.telegram.org/bots/features#botfather)  
- `TELEGRAM_OWNER_ID` - ваш личный ID от Telegram (выглядит как 123456789). Узнать можно следующим образом:  
Добавьте в список контактов бота `@MyTelegramID_bot`.  
Начните с ним диалог командой `/start`, в ответном сообщении вы узнаете цифры идентификатора.  
Можете использовать также бота `@GetMyIDBot` или `@my_id_bot` для этой же цели.  


- `SECRET_KEY` - секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
   Получить секретный ключ Django:
```shell
python
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
```
- `STRIPE_API_KEY` - API-ключ, [полученный из платежной системы STRIPE.](https://stripe.com/docs/keys#create-api-secret-key)
- `DEBUG` - режим отладки. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
Выключается значением `False`.
- `ALLOWED_HOSTS` - по умолчанию: localhost, 127.0.0.1. [документация Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `STATIC_ROOT` - папка для сбора статики сайта при размещении на сервере, например "assets". Нельзя задавать "static".  
- `CSRF_TRUSTED_ORIGINS=http://subdomen.domen.com` - домен/субдомен сайта.  

Для запуска проекта следующие настройки менять не требуется, значения проставлены для деплоя.  
- `SECURE_HSTS_SECONDS=10`  
- `SESSION_COOKIE_SECURE=True`  
- `CSRF_COOKIE_SECURE=True`  
- `SECURE_HSTS_PRELOAD=True`  
- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`  
- `SECURE_SSL_REDIRECT=True`  
[документация по настройкам Django Deployment checklist](https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/).  


## Запуск
- Установите зависимости командой `pip install -r requirements.txt`
- Создайте файл базы данных и сразу примените все миграции командой `python manage.py migrate`
- Запустите сервер командой `python manage.py runserver`
- Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Администрирование
- Откройте новую панель командной строки.
- Для регистрации администратора сайта введите команду `python manage.py createsuperuser`,  
    после чего введите выбранный вами логин, e-mail и пароль администратора (2 раза).  
- При вводе пароля символы не отображаются. Ввод завершается нажатием Enter.  
- Затем запустите сервер для администрирования командой `python manage.py runserver`
- Перейдите по адресу http://127.0.0.1:8000/admin
- Используйте данные для авторизации (Username: Password:, введенные чуть ранее)


Основной вид административной панели в разделе "Заказы":  
![Orders](https://github.com/Kisly93/FlowersShop/assets/111083714/db7b6b72-3e61-461d-9717-e6f02ff71d8d)

Основной вид административной панели в разделе "Букеты":
![Bouquets](https://github.com/Kisly93/FlowersShop/assets/111083714/c6b8f2ca-98f1-4dfe-845c-43d7066da0c8)


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
