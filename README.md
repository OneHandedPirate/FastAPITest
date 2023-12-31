# Тестовая задача

## Описание задачи

Реализуйте REST-сервис просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности, вам
потребуется реализовать метод где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.

Необязательные технические требования (по возрастанию трудоемкости):
- написаны тесты с использованием pytest;
- реализована возможность собирать и запускать контейнер с сервисом в Docker.


### Реализация:

API на FastAPI с подключенной через SQLAlchemy Postgres.

### Требования:
 - Поднятая Postgres


Установка:
- Стянуть репо проекта:<br>`git clone https://github.com/OneHandedPirate/FastAPITest.git` <br>в отдельную директорию<br>
- В этой директории создать виртуальное окружение:<br>`python3 -m virtualenv venv` <br> (если virtualenv не установлен - установить командой `pip install virtualenv`)
- Активировать виртуальное окружение:<br>
 Linux: `source venv/bin/activate` <br>Windows: `venv\Scripts\activate.bat`
- Установить зависимости проекта: <br>`pip install -r requirements.txt`
- Создать `.env` файл в корне проекта со следующим набором переменных:<br>
    `POSTGRES_USER` - пользователь postgres;<br>
    `POSTGRES_PASSWORD` - пароль postgres;<br>
    `POSTGRES_DB` - БД postgres;<br>
    `POSTGRES_HOST` - хост postgres;<br>
    `POSTGRES_PORT` - порт postgres (по умолчанию: 5432);<br>
    `SECRET_KEY` - секретный ключ, длинная строка, используется для создания JWT-токена;<br>
    `JWT_EXPIRATION_TIME` - время, в течение которого токен будет валидным (в минутах) токена в минутах;<br>
    `JWT_ALGORITHM` - алгоритм JWT-токена (по умолчанию: HS256);<br>
  

  * Переменные задавать в виде `<имя>=<значение>` без пробелов, иначе докер ругается.

### Запуск:
- Для запуска в системе:<br>
`uvicorn app.main:app --reload`<br>
По умолчанию будет висеть на 8000 порту, для изменения порта при запуске можно указать ключ `--port` и через пробел желаемый порт. 
- Для запуска в контейнере:<br>
  1. Собрать образ командой<br> `docker build . -t <имя образа>`
  2. Запустить контейнер, пробросив порт и указав файл с переменными<br>`docker run -p <желаемый порт>:8000 --env-file .env <имя образа>`


### Описание эндпоинтов:
- `/create_account` - эндпоинт для создания объектов `User`. <br>Метод: `POST`. <br>Принимает JSON в body вида: <br>`{"username": <имя пользователя>, "password": <пароль>}`<br>Проверяет `username` на уникальность, далее хэширует пароль (используется библиотека passlib) и передает объект в БД. Далее создается объект `Employee`, связанный с созданным юзером, с рандомными данными в полях `salary` и `promotion_date`. Для валидации входящих данных используется pydantic-модель. Данные являются валидными если длина username не меньше 5 символов, а длина пароля - не меньше 8.
- `/login` - эндпоинт для логина и выдачи JWT. <br>Метод: `POST`. <br>Принимает форму (`application/x-www-form-urlencoded`) c кредами. Последовательно проверяет `username` и пароль (хэширует и сверяет с хэшированным паролем в БД). После проверки выдает JWT с id юзера и временем истечения валидности токена в payload.
- `/get_info` - эндпоинт для проверки своих данных. <br>Метод: `GET`. <br>Проверяет, если ли в заголовке `Authorization` валидный JWT-токен. Если есть - проверяет, есть ли `User` в БД (есть вероятность, хотя она невелика, что токен до сих пор валидный, но юзера уже нет в базе, тогда возникнет исключение 404). Если все проверки прошли - `User` видит в ответе данные о своей зарплате и дате следующего повышения.
- `/delete_account/{username}` - эндпоинт для удаления аккаунта по `username`. <br>Метод: `GET`.<br>Проверяет только наличие объекта User переданным username. Если проверка пройдена - удаляет его. Добавлен для простоты тестирования.

### Тесты:
В `test_main.py` добавлено 10 тестов. Запуск тестирования - командой `pytest`.


### **Все команды терминала выполнять в корневой папке проекта.