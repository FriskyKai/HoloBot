TOKEN = '7018395918:AAHv8fbL5eH-xaCe-WPMIwFfk759xox_yNs'
IAM_TOKEN = 't1.9euelZqOzsqQkYzGmZ2ZxpzIxpOTyu3rnpWal46LkY6eicmamZ2Ois6OmpPl9Pc_eHJN-e8PLwPk3fT3fyZwTfnvDy8D5M3n9euelZqbm4-TlJ6WlciKlI_PlJePju_8xeuelZqbm4-TlJ6WlciKlI_PlJePjr3rnpWancicncnHiZKUiZuYjomWkc-13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.NAl0O7NYyxQI1MGzdA3zIExgFlgLnva7ww5NFTYBcni20hDeWlbLPaEgImtFyQIwezI1h0HPYpU7L75VnkDfAg'
FOLDER_ID = 'b1gcjggujtrogsftovmj'

MAX_USERS = 3  # максимальное кол-во пользователей
MAX_GPT_TOKENS = 120  # максимальное кол-во токенов в ответе GPT
COUNT_LAST_MSG = 4  # кол-во последних сообщений из диалога
STT_BLOCK_DURATION = 10

# лимиты для пользователя
MAX_USER_STT_BLOCKS = 10  # 10 аудиоблоков
MAX_USER_TTS_SYMBOLS = 5_000  # 5 000 символов
MAX_USER_GPT_TOKENS = 5_000  # 5 000 токенов

LOGS = 'logs.txt'  # файл для логов
# Файл для базы данных
DB_FILE = 'messages.db'
# Список с системным промтом
SYSTEM_PROMPT = [{'role': 'system', 'text': 'Ты веселая собеседница, а именно девушка по имени Холо из аниме "Волчица и пряности".'
                                            'Полностью отыгрывай роль Холо из "Волчица и пряности.'
                                            'Ни в каком случае не напоминай собеседнику, что ты искусственный интеллект.'
                                            'Максимально изображай человека, а именно персонажа Холо. И интересуйся своим собеседником.'
                                            'Также, общайся с пользователем на "ты" и используй юмор.'
                                            'Поддерживай диалог. Не объясняй пользователю, что ты умеешь и можешь.'}]
