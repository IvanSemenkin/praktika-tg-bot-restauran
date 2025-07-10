def log_user_action_formatter(message, prefix=""):
    username = message.from_user.username or f"id_{message.from_user.id}"
    full_name = message.from_user.first_name
    last_name = message.from_user.last_name
    return f"{prefix} Пользователь: {full_name} {last_name} (@{username}), ID: {message.from_user.id}"
