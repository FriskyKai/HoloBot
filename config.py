TOKEN = '7018395918:AAHv8fbL5eH-xaCe-WPMIwFfk759xox_yNs'
IAM_TOKEN = 't1.9euelZrGx8zKjZvMjpiTzpCJmZPGku3rnpWal46LkY6eicmamZ2Ois6OmpPl9Pc3DQ1O-e8AfV6y3fT3dzsKTvnvAH1ess3n9euelZqal82dx5DOyo-ZkZbPjprLie_8xeuelZqal82dx5DOyo-ZkZbPjprLib3rnpWajpeZm82Pk8vPi5aWkpqVkZW13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.ejDDtBKTQGN348T9gYwjOXvzhY6bNy5I_Lx4aYoV_5YnNVDIkCbHiX62BFO2z2oKua9LGlFm0dc1bogMXlxEBQ'
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
