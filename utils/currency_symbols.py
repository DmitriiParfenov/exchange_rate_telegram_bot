import json
import os

import requests

EXCHANGE_RATE_API_KEY = os.environ.get('EXCHANGE_RATE_API_KEY')


def get_currency_symbols(symbol=None):
    """
    Фунция возвращает список доступных символов валют для конвертации от API.
    Есть необязательный аргумент symbol, который позволяет проверить, если данная валюта в списке
    доступных.
    :param symbol: str
    :return: str
    """
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    response = requests.get(url, headers={'apikey': EXCHANGE_RATE_API_KEY})
    if response.ok:
        response_data = json.loads(response.text)
        result = {}
        if symbol is None:
            result = response_data["symbols"]
            return result
        else:
            if response_data['symbols'].get(symbol):
                result += f'{symbol} — {response_data["symbols"][symbol]}\n'
                return result
            else:
                return f'Нет такого символа валюты'
    else:
        return f'Некорректный ответ сервера'
