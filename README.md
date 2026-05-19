# Прогнозирование динамики банковских переводов юридических лиц

**Cтудент: Северенкова Анастасия Евгеньевна**
**Научный руководитель: Левченко Любовь Леонидовна**

## Данные 
Данные для иследовательской рабоыт взяты из соревнования https://ods.ai/competitions/data-fusion2025-4cast/dataset - https://ods.ai/competitions/data-fusion2025-4cast/dataset. Задача соревнования заключается в прогнозировании временных рядов денежных переводов для клиентов банка. Анализ ряда по целевой переменной выполнен в файле /research/lightGBM_sarima(1).ipynb

## Метрика 
Метрика качества соответсвует заявленной в соревновании - RMSLE. 
$$\overline{RMSLE} = \frac{1}{N}\sum_{i=1}^N \sqrt{\frac{1}{T}\sum_{t=1}^T (\log(1+y_{it}) - \log(1+\hat{y}_{it}))^2}$$

## Базовое предсказание 
Базовое предсказание на модели lightGBM
Работа в в файле /research/lightGBM_sarima(1).ipynb

| модель   | public score 1 место | полученный score |
|----------|-----------------------|------------------|
| lightGBM | 1,41                  | 1, 46            |  
|          |                       |                  |   

## Экспериментальная часть 
- исследование доп данных в файле /research/eda_transactions.ipynb
- эксперименты с CatBoost в файле /research/transactions_catboost.ipynb
- базовое предсказание на XGBoost в файле /transactions_xgboost.ipynb
- добавлена обработка кат признаков в /transactions_xgboost.ipynb
- сравнение нескольких наборов признаков в /transactions_xgboost.ipynb
- реализация mvp-сервиса для модели в директории /service 
- финальный вариант ВКР в /transactions_xgboost.ipynb

## Финальный вариант 
XGBoost + лаги по 70 неделям, прогнозирование на k периодов, логарифмирование - **score 1,82 на private** 