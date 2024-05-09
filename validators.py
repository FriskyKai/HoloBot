import logging  # модуль для сбора логов
import math  # математический модуль для округления
# подтягиваем константы из config файла
from config import *
# подтягиваем функции для работы с БД
from database import count_users, count_all_limits
# подтягиваем функцию для подсчета токенов в списке сообщений
from yandex_gpt import count_gpt_tokens

# настраиваем запись логов в файл
logging.basicConfig(filename=LOGS, level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")


# получаем количество уникальных пользователей, кроме самого пользователя
def check_number_of_users(user_id):
    count = count_users(user_id)
    if count is None:
        return None, "Ошибка при работе с БД"
    if count > MAX_USERS:
        return None, "Превышено максимальное количество пользователей"
    return True, ""


# проверяем, не превысил ли пользователь лимиты на общение с GPT
def is_gpt_token_limit(messages, total_spent_tokens):
    all_tokens = count_gpt_tokens(messages) + total_spent_tokens
    if all_tokens > MAX_USER_GPT_TOKENS:
        return None, f"Превышен общий лимит GPT-токенов {MAX_USER_GPT_TOKENS}"
    return all_tokens, ""


# проверяем, не превысил ли пользователь лимиты на преобразование аудио в текст
from config import MAX_USER_STT_BLOCKS, STT_BLOCK_DURATION


def is_stt_block_limit(user_id, duration):
    try:
        used_stt_blocks = count_all_limits(user_id, 'stt_blocks')
        remaining_stt_blocks = MAX_USER_STT_BLOCKS - used_stt_blocks

        if remaining_stt_blocks <= 0:
            return None, f"Превышен лимит аудиоблоков для распознавания текста ({MAX_USER_STT_BLOCKS})"

        # Рассчитываем количество требуемых аудиоблоков для данного аудио
        blocks_needed = math.ceil(duration / STT_BLOCK_DURATION)

        if blocks_needed > remaining_stt_blocks:
            return None, f"Для данного аудио требуется {blocks_needed} аудиоблоков, но доступно только {remaining_stt_blocks}"

        return blocks_needed, ""
    except Exception as e:
        logging.error(e)
        return None, "Ошибка при проверке лимита аудиоблоков для распознавания текста"


# проверяем, не превысил ли пользователь лимиты на преобразование текста в аудио
def is_tts_symbol_limit(user_id, text):
    try:
        # Получаем количество использованных символов для TTS
        used_tts_symbols = count_all_limits(user_id, 'tts_symbols')

        # Проверяем, сколько символов осталось до достижения лимита
        remaining_tts_symbols = MAX_USER_TTS_SYMBOLS - used_tts_symbols

        if remaining_tts_symbols <= 0:
            return None, f"Превышен лимит символов для синтеза речи ({MAX_USER_TTS_SYMBOLS})"

        # Проверяем, сколько символов потребуется для данного текста
        symbols_needed = len(text)

        if symbols_needed > remaining_tts_symbols:
            return None, f"Для данного текста требуется {symbols_needed} символов для синтеза речи, но доступно только {remaining_tts_symbols}"

        return symbols_needed, ""
    except Exception as e:
        logging.error(e)
        return None, "Ошибка при проверке лимита символов для синтеза речи"
