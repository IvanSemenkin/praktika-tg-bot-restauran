from src.utils.logger import logger

def log_user_action(message, prefix):
    user = message.from_user
    username = user.username or f"id_{user.id}"
    full_name = user.first_name or ""
    last_name = user.last_name or ""
    log_msg = f"{prefix} Пользователь: {full_name} {last_name} (@{username}), ID: {user.id}"
    logger.info(log_msg)
