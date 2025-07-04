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

## Запуск

1. Запустить Redis на порту 6380.
2. Запустить Ollama:
   ```bash
   ollama serve
3. `pip install -r requirements.txt`
4. `python main.py`
