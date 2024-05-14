import os
import telebot
import logging
from validators import *  # модуль для валидации
from speechkit import *  # модуль для работы с SpeechKit
from yandex_gpt import ask_gpt  # модуль для работы с GPT
# подтягиваем константы из config файла
from config import TOKEN, LOGS, COUNT_LAST_MSG
# подтягиваем функции из database файла
from database import create_database, add_message, select_n_last_messages

# настраиваем запись логов в файл
logging.basicConfig(filename=LOGS, level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")
logging.basicConfig(filename=LOGS, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)


def main():
    # Тестовая команда /stt
    @bot.message_handler(commands=['stt'])
    def stt_handler(message):
        logging.info('INFO: Вызван метод stt...')
        user_id = message.from_user.id
        bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')
        bot.register_next_step_handler(message, stt)

    def stt(message):
        user_id = message.from_user.id

        if not message.voice:
            return

        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        bot.send_message(user_id, 'Активно пишу...')

        status, text = speech_to_text(file)

        if status:
            bot.send_message(user_id, text, reply_to_message_id=message.id)
        else:
            bot.send_message(user_id, text)

    # Тестовая команда /tts
    @bot.message_handler(commands=['tts'])
    def tts_handler(message):
        logging.info('INFO: Вызван метод tts...')
        user_id = message.from_user.id
        bot.send_message(user_id, 'Отправь текстовое сообщение, чтобы я его озвучил!')
        bot.register_next_step_handler(message, tts)

    def tts(message):
        user_id = message.from_user.id
        text = message.text

        if message.content_type != 'text':
            bot.send_message(user_id, 'Отправь текстовое сообщение')
            return

        bot.send_message(user_id, 'Озвучиваю...')

        status, content = text_to_speech(text)

        if status:
            bot.send_voice(user_id, content)
        else:
            bot.send_message(user_id, content)

    # Команда /debug
    @bot.message_handler(commands=['debug'])
    def debug(message):
        try:
            filepath = 'logs.txt'

            # Проверяем существование файла и его размер
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                # Отправляем файл как документ
                with open(filepath, 'rb') as f:
                    bot.send_document(message.chat.id, f)
            else:
                # Файл пустой или не найден, отправляем сообщение
                if os.path.exists(filepath):
                    bot.send_message(message.chat.id, 'Файл logs.txt пустой.')
                else:
                    bot.send_message(message.chat.id, 'Файл logs.txt не найден.')
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')

    # Текстовые сообщения
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        try:
            user_id = message.from_user.id

            # ВАЛИДАЦИЯ: проверяем, есть ли место для ещё одного пользователя (если пользователь новый)
            status_check_users, error_message = check_number_of_users(user_id)

            if not status_check_users:
                bot.send_message(user_id, error_message)  # мест нет =(
                return

            # БД: добавляем сообщение пользователя и его роль в базу данных
            full_user_message = [message.text, 'user', 0, 0, 0]
            add_message(user_id=user_id, full_message=full_user_message)

            # ВАЛИДАЦИЯ: считаем количество доступных пользователю GPT-токенов
            # получаем последние 4 (COUNT_LAST_MSG) сообщения и количество уже потраченных токенов
            last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)
            # получаем сумму уже потраченных токенов + токенов в новом сообщении и оставшиеся лимиты пользователя
            total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)

            if error_message:
                # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
                bot.send_message(user_id, error_message)
                return

            # GPT: отправляем запрос к GPT
            status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
            # GPT: обрабатываем ответ от GPT
            if not status_gpt:
                # если что-то пошло не так — уведомляем пользователя и прекращаем выполнение функции
                bot.send_message(user_id, answer_gpt)
                return
            # сумма всех потраченных токенов + токены в ответе GPT
            total_gpt_tokens += tokens_in_answer

            # БД: добавляем ответ GPT и потраченные токены в базу данных
            full_gpt_message = [answer_gpt, 'assistant', total_gpt_tokens, 0, 0]
            add_message(user_id=user_id, full_message=full_gpt_message)

            bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)  # отвечаем пользователю текстом
        except Exception as e:
            logging.error(e)  # если ошибка — записываем её в логи
            bot.send_message(message.from_user.id, "Не получилось ответить. Попробуй написать другое сообщение")

    # Голосовые сообщения
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message: telebot.types.Message):
        try:
            user_id = message.from_user.id

            # Проверка на максимальное количество пользователей
            status_check_users, error_message = check_number_of_users(user_id)

            if not status_check_users:
                bot.send_message(user_id, error_message)
                return

            # Проверка на доступность аудиоблоков
            stt_blocks, error_message = is_stt_block_limit(user_id, message.voice.duration)

            if error_message:
                bot.send_message(user_id, error_message)
                return

            # Обработка голосового сообщения
            file_id = message.voice.file_id
            file_info = bot.get_file(file_id)
            file = bot.download_file(file_info.file_path)
            status_stt, stt_text = speech_to_text(file)

            if not status_stt:
                bot.send_message(user_id, stt_text)
                return

            # Запись в БД
            add_message(user_id=user_id, full_message=[stt_text, 'user', 0, 0, stt_blocks])

            # Проверка на доступность GPT-токенов
            last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)

            total_gpt_tokens, error_message = is_gpt_token_limit(last_messages, total_spent_tokens)

            if error_message:
                bot.send_message(user_id, error_message)
                return

            # Запрос к GPT и обработка ответа
            status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
            if not status_gpt:
                bot.send_message(user_id, answer_gpt)
                return
            total_gpt_tokens += tokens_in_answer

            # Проверка на лимит символов для SpeechKit
            tts_symbols, error_message = is_tts_symbol_limit(user_id, answer_gpt)

            # Запись ответа GPT в БД
            add_message(user_id=user_id, full_message=[answer_gpt, 'assistant', total_gpt_tokens, tts_symbols, 0])

            if error_message:
                bot.send_message(user_id, error_message)
                return

            # Преобразование ответа в аудио и отправка
            status_tts, voice_response = text_to_speech(answer_gpt)
            if status_tts:
                bot.send_voice(user_id, voice_response, reply_to_message_id=message.id)
            else:
                bot.send_message(user_id, answer_gpt, reply_to_message_id=message.id)
        except Exception as e:
            logging.error(e)
            bot.send_message(user_id, "Не получилось ответить. Попробуй записать другое сообщение")

    bot.polling()


if __name__ == "__main__":
    main()
