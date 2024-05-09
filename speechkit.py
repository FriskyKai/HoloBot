import requests
from config import *


# Голос в текст
def speech_to_text(data):
    iam_token = IAM_TOKEN
    folder_id = FOLDER_ID

    headers = {
        'Authorization': f'Bearer {iam_token}',
    }

    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])

    response = requests.post(
        f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
        headers=headers,
        data=data
    )

    decoded_data = response.json()

    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        return False, "При запросе в SpeechKit возникла ошибка"


# Текст в голос
def text_to_speech(text):
    iam_token = IAM_TOKEN
    folder_id = FOLDER_ID

    headers = {
        'Authorization': f'Bearer {iam_token}',
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'marina',
        'folderId': folder_id,
    }
    # Выполняем запрос
    response = requests.post(
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers=headers,
        data=data
    )
    if response.status_code == 200:
        return True, response.content  # возвращаем статус и аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"

