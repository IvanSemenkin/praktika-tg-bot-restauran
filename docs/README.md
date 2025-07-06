# FoodBot

Telegram-бот с ИИ, который помогает выбирать еду, предлагать блюда и сочетания продуктов. Хранит историю диалогов пользователей в Redis через FSM.

## Возможности

### Команды пользователя

* “ИИ” — запуск режима общения с ботом по еде.
* `/info` — история последних сообщений.
* `/del_my_info` — удалить свою историю.

### Команды админа

* `/get_all_key` — все ключи Redis.
* `/get_info_id` — история по ID.
* `/del_info_id` — удалить историю по ID.
* `/cls` — очистить всю БД.

## Используемые технологии

* Python, Aiogram 3
* Redis + aiogram-fsm-storage-redis
* LangChain + FAISS
* LLaMA 3.1 (через localhost)
* Асинхронный фреймворк для создания Telegram ботов.

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


## Запуск

#### 1. Запустить Redis

```bash
redis-cli 
```

#### 2. Запустить Ollama

```bash
ollama serve
```

#### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

#### 4. Настроить переменные окружения

Создайте файл `.env` в корне проекта и добавьте следующие строки:

```env
TOKEN=ваш_токен_бота_telegram
BASE_URL=url_для_запросов_ии
LOG_LEVEL=DEBUG
REDIS_HOST=localhost
REDIS_PORT=ваш_порт_redis'а
```

#### 5. Запустить бота

```bash
python main.py
```


## Автор

**Иван Семенкин**  
[isemenkin@gmail.com](mailto:isemenkin@gmail.com)

[GitHub](https://github.com/IvanSemenkin)