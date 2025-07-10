import redis
import json
import sys
from typing import Dict, List

def get_redis_connection(host: str = 'localhost', port: int = 6380, db: int = 0) -> redis.Redis:
    """Устанавливает соединение с Redis"""
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)

def list_user_ids(r: redis.Redis) -> List[str]:
    """Возвращает список всех ID пользователей с историей"""
    keys = r.keys('fsm:*:data')
    return list(set(key.split(':')[1] for key in keys))

def get_chat_history(r: redis.Redis, user_id: str) -> List[Dict[str, str]]:
    """Получает историю переписки для конкретного пользователя"""
    key = f'fsm:{user_id}:{user_id}:data'
    data = r.get(key)
    if not data:
        return []
    
    try:
        parsed = json.loads(data)
        return parsed.get('history', [])
    except json.JSONDecodeError:
        return []

def format_history(history: List[Dict[str, str]]) -> str:
    """Форматирует историю в читаемый вид"""
    formatted = []
    for msg in history:
        role = "Пользователь" if msg['role'] == 'user' else "Бот"
        formatted.append(f"{role}: {msg['content']}")
    return '\n'.join(formatted)

def main():
    # Подключаемся к Redis
    r = get_redis_connection()
    
    # Получаем список доступных ID пользователей
    user_ids = list_user_ids(r)
    
    if not user_ids:
        print("Нет доступных ID пользователей с историей переписки")
        sys.exit(0)  # Завершаем работу
    
    print(f"Доступные ID пользователей: {', '.join(user_ids)}")
    
    # Запрашиваем ID пользователя
    user_id = input("\nВведите ID пользователя для просмотра истории: ")
    
    # Получаем и выводим историю
    history = get_chat_history(r, user_id)
    if not history:
        print(f"История для пользователя {user_id} не найдена")
        return
    
    print("\nИстория переписки:")
    print(format_history(history))

if __name__ == "__main__":
    main()