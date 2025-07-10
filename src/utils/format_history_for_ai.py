def format_history_for_ai(history: list) -> str:
    """Форматирует историю диалога для передачи ИИ"""
    history_text = []
    for msg in history:
        if msg["role"] == "user":
            history_text.append(f"Пользователь: {msg['content']}")
        else:
            history_text.append(f"Ассистент: {msg['content']}")
    return "\n".join(history_text)