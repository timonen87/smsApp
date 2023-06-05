# SMS Mailing Сервис рассылки сообщений с возможностью отложенной отправки сообщений

Django / djangorestframework / Celery / Redis / Flower


## Запуск проекта

1. Клонируем репозиторий с github.com:

````
git@github.com:timonen87/smsApp.git
````
2. Заходим в директорию проекта
````
cd smsApp
````

3. Создем и активируем виртуальное окружение:

````
python3 -m venv env
source env/bin/activate
````

4. В файле .env настариваем переменные окуружения: 
 
5. Устанавливаем зависимости, создаем миграции и запускаем сервер:

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

6 Настариваем логирование задач, для этого создаем папку logs/celery.log в корневой директории

7. Запускаем менеджер задач celery ()

```
celery -A core.celery.app worker --loglevel=info --logfile=logs/celery.log
```
10. Запускаем flower

```
celery -A core.celery.app flower
```
***
### Запуск тестов
``` 
python manage.py test
```
***
## Установка с  docker-compose


1. Клонируем репозиторий с github.com:
```
git@github.com:timonen87/smsApp.git
```
2. Заходим в директорию проекта
````
cd smsApp
````

3. В файле .env настариваем переменные окуружения:

4. Запускаем сборку контейнеров
``` 
sudo docker-compose build
 ```
5. Запускаем сборку 
```
sudo docker-compose up -d
```

## API методы 
***

```http://0.0.0.0:8080/api/clients/``` - все клиенты

```http://0.0.0.0:8080/api/mailings/``` - все рассылки постранично

```http://0.0.0.0:8080/api/mailings/fullstat/``` - общая статистика по всем рассылкам

```http://0.0.0.0:8080/api/mailings/<pk>/totalstat/``` - статистика по каждому сообщению из рассылки

```http://0.0.0.0:8080/api/messages/``` - все сообщения постранично

```http://0.0.0.0:8080/api/schema/``` - OpenApi schema 

```http://0.0.0.0:8080/api/docs/``` - swagger api

```http://0.0.0.0:8080/api/redoc/``` - документация api методов

```http://0.0.0.0:5555``` -  просмотр задач celery flower

***