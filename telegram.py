import requests
from dotenv import load_dotenv
import json
import pprint as pp

load_dotenv()
TOKEN = "7254863788:AAFv34POqwiiP9OibnBkds1r88oNSJisjmM"
CHAT_IDS = ["1023428187"]
TIMEOUT = 10  # Timeout in seconds

def send_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    for chat_id in CHAT_IDS:
        parameters = {'chat_id': chat_id, 'text': text}
        try:
            response = requests.post(url, parameters, timeout=TIMEOUT)
            response.raise_for_status()
            result = response.json()
            if not result.get('ok'):
                print(f"Failed to send message to {chat_id}: {result}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending message to {chat_id}: {e}")
    return response

def send_photo(photo_file):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    for chat_id in CHAT_IDS:
        parameters = {'chat_id': chat_id}
        try:
            response = requests.post(url, parameters, files={'photo': photo_file}, timeout=TIMEOUT)
            response.raise_for_status()
            result = response.json()
            if not result.get('ok'):
                print(f"Failed to send photo to {chat_id}: {result}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending photo to {chat_id}: {e}")
    return response

if __name__ == "__main__":
    print('Sending a test message.')
    response = send_message('Testing')
    response_json = json.loads(response.text)
    print('Results:')
    pp.pprint(response_json)
    assert response_json['ok']

    with open('archive/test.png', 'rb') as f:
        response = json.loads(send_photo(f).text)
    pp.pprint(response)
    assert response['ok']
