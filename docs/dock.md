# FOODBOT

## Структура проекта

```bash
food-combo-bot/
│
├── main.py
├── docs/
│   ├── pyproject.toml
│   └── README.md
├── knowledge_base/
│   ├── cuisine/
│   ├── dishes/
│   ├── meal_time/
│   ├── situation/
│   ├── taste/
│   └── weather/
├── src/
│   ├── bot/
│   │   ├── ai.py
│   │   ├── handlers.py
│   │   ├── hendlers.py
│   │   ├── keyboards.py
│   │   └── states.py
│   └── storage/
│       ├── utils/
│       │   ├── log_user_action.py
│       │   ├── logger.py
│       │   └── prompt.py
```

## Используемые технологии
* <img src="https://img.icons8.com/color/48/000000/python.png" width="16" height="16" alt="Python"/> Python (основной язык)
* <img src="https://img.icons8.com/?size=100&id=oWiuH0jFiU0R&format=png&color=000000" width="16" height="16" alt="Python"/> aiogmar (Библиотека для ТГ бота)
* <img src="https://img.icons8.com/color/48/000000/redis.png" width="16" height="16" alt="Redis"/> Redis (Работа с БД)
* <img src="https://img.icons8.com/?size=100&id=POBc2SrrhhnF&format=png&color=000000" width="16" height="16" alt="Redis"/> LangChain (Работа с ИИ) 

## Виртуальные переменные <img src="https://img.icons8.com/?size=100&id=1yJTo23YkTV3&format=png&color=000000" width="32" height="32" alt="Redis"/>
### В файле .env необходимо установить виртуальные переменные:
```ini
TOKEN=токен_вашего_тг_бота_из_botfather
GROQ_API_KEY=ваш_токен_groq
LOG_LEVEL=DEBUG
REDIS_HOST=хост_redis(localhos)
REDIS_PORT=порт_redis(6379)
REDIS_DB=номер_таблицы_redis(0)
```

#### [Groq](https://groq.com/) <-- там можно взять API-ключ
#### [BotFather](https://t.me/BotFather) <-- там можно создать бота и получить токен


## Работа с ботом
* При запуске бота можно запустить ИИ нажав на соответствующую кнопку
* После появятся 2 кнопки `Сочитаемость блюд` и `Выбор блюд`
