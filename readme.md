# Навык для Алисы Яндекса - открыть дверь домофона
## Вводные
Есть устройство - [Яндекс.Станция](https://yandex.ru/alice/station)
Есть домофон, управляемый с помощью мобильного приложения ["Мой умный дом"](https://play.google.com/store/apps/details?id=ru.ufanet.smarthome&hl=ru&gl=US), разработанного компанией [Уфанет](https://www.ufanet.ru/)

Хотелось сделать что-нибудь, чтобы Алиса открывала дверь домофона.

## Что получилось
С помощью [mitmproxy](https://mitmproxy.org/) расковырял авторизацию мобильного приложения перед  API ufanet.
На Python+Fastapi+Postgres нарисовал сервис с API, который может регистрировать двери в БД Postgres и открывать их по команде Алисы.
Сервис запаковывается в Docker-контейнер и может быть доступен через https. Сертификат для домена получаем от [LetsEncrypt](https://letsencrypt.org/).
Сервис хостится на [gandi.net](https://www.gandi.net/)

### Переменные окружения
Файл .env.prod содержит переменные окружения для проекта в виде ENV_VAR=VALUE

- DEBUG - True - включает отладочные логи (По умолчанию - False)
- DB_CONNECTION - строка подключения к БД postgres: postgresql://postgres:postgres@<postgres host>:<postgres port>/postgres
- OPENAPI_JSON_URL - OpenAPI json URL - путь к json файлу OpenAPI (по умолчанию - пустая строка, если надо чтобы OpenAPI было доступно - здесь должен быть URL, например "/openapi.json")
- OPENAPI_DOCS_PATH - путь Swagger ui (по умолчанию - пустая строка, если надо чтобы Swagger UI было доступно - здесь должен быть URL, например "/docs")
- OPENAPI_REDOC_PATH - путь ReDoc ui (по умолчанию - пустая строка, если надо чтобы ReDoc UI было доступно - здесь должен быть URL, например "/redoc")
- RESTRICTED_PATH_Х - (Х = 1, 2, 3, и т.д.) - URL API с ограниченным доступом - например: /domofon/register*
- ALLOWED_HOSTS_FOR_PATH_1 - (Х = 1, 2, 3, и т.д.) - список хостов, которым разрешен доступ к API RESTRICTED_PATH_Х - например: 127.0.0.1,localhost,192.168.0.*
- API_KEY - ключ API gandi.net
- CERTBOT_DOMAIN - домен, для которого получаем/обновляем сертификат LetsEncrypt, например api.example.com

### Деплой
- Делаем git clone с этого репозитория например, в папку, /opt
- Устанавливаем cretbot, например: 
``` bash 
sudo apt install certbot
```
- Запускаем скрипт создания системного кронтаба: 
``` bash 
sudo ./certbot-crontab-create.sh
```
- Создаем контейнер: Делаем 
``` bash 
docker-compose -f docker-compose-prod.yml build
```
- Создаем сервис systemd, который будет запускать контейнер: кладем файл domofon.service в директорию /etc/systemd/system
- запускаем БД:
``` bash 
docker-compose -f docker-compose-prod.yml up -d db
```
- выполняем скрипты миграции:
``` bash 
alembic upgrade head
```
- останавливаем сервис :
``` bash 
docker-compose -f docker-compose-prod.yml down
```
- Запускаем сервис: 
``` bash 
sudo systemctl start domofon
```
- Регистрируем дверь в нашем сервисе:
Выполняем POST запрос
``` 
https://local_service_host:8000/api/v1/domofon/register
```
с заголовком
``` 
Content-type: application/json
```
и телом
``` json
{
	"door": 
	{
		"door_id" : <ID двери (придумайте сами)>,
		"ext_door_id" : "",
		"ext_user": <login в приложении "Мой умный дом">,
		"ext_password" : <пароль в приложении "Мой умный дом">
	}
}
```
- Если наш хост находится за NATом - пробрасываем на роутере порт на хост с нашим сервисом
- [Создаем в Алисе навык](https://dialogs.yandex.ru/developer), прописываем туда ссылку на наш сервис с параметром - ID двери, публикуем навык
``` 
https://<remote_service_domain>:8000/api/v1/domofon/aliceopen?door_id=<ID двери>
```
- Если все получилось, то на кодовую фразу, например, "Алиса, попроси домофон открыть дверь" - дверь домофона открывается.