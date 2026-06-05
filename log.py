import logging
import logging.handlers
import os
from aiogram.types import Message


# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
def setup_logging():
    """Настройка ротируемых логов (макс 2 MB, 1 резервная копия)"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'bot.log')

    # Ротация: при достижении 2 MB создаётся bot.log.1, старый удаляется
    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,  # 2 MB
        backupCount=1,  # храним только 1 старый файл
        encoding='utf-8'
    )

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Получаем корневой логгер
    logger = logging.getLogger('bulls_and_cows')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Также выводим в консоль (полезно для отладки)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


# Инициализируем логгер
logger = setup_logging()


def log_user_info(message: Message, action: str, extra_info: str = ""):
    """Логирует информацию о пользователе"""
    user = message.from_user
    user_info = (
        f"👤 {action} | "
        f"ID: {user.id} | "
        f"Username: @{user.username or 'нет'} | "
        f"Имя: {user.first_name or ''} {user.last_name or ''} | "
        f"Язык: {user.language_code or 'неизвестен'}"
    )
    if extra_info:
        user_info += f" | {extra_info}"

    logger.info(user_info)

    # Дополнительно: если есть номер телефона (только если пользователь его отправил)
    if hasattr(user, 'phone_number') and user.phone_number:
        logger.info(f"📱 Телефон: {user.phone_number}")