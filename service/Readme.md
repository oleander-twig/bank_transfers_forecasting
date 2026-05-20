## Первый запуск приложения 
1. Запустить приложение `docker compose up --build`
2. Загрузить модель с помощью скрипта `helpers/upload_model.py`
3. Накатить необходимые миграции с помощью `helpers/run_migrations.py`
4. Пример запроса
```
curl --location '0.0.0.0:8000/predict' \
--header 'Content-Type: application/json' \
--data '{
    "inn_list":["inn1000051"]
}'
```