import json
import os
from datetime import datetime as dt

import requests

EXCHANGE_RATE_API_KEY = os.environ.get('EXCHANGE_RATE_API_KEY')


class ExchangeRate:
    """Класс для получения курса валют от API"""
    def __init__(self, key, from_currency, to_currency):
        self.key = key
        self.from_currency = from_currency.upper()
        self.to_currency = to_currency.upper()
        self._result = {}
        self._data = ''
        self._currency_data_file = "currency_rates.json"

    def get_currency_rate(self, amount=1):
        url = "https://api.apilayer.com/exchangerates_data/latest"
        params = {'symbols': self.to_currency, 'base': self.from_currency}
        response = requests.get(url, headers={'apikey': self.key}, params=params)
        if response.ok:
            response_data = json.loads(response.text)
            timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            for elem in response_data["rates"]:
                self._result = {elem: response_data["rates"][elem] * amount}
            data = {"from_currency": self.from_currency,
                    "to_currency": self.to_currency,
                    "rate": self._result[self.to_currency],
                    "timestamp": timestamp}
            self.save_to_json(data)
        else:
            return f'Некорректный ответ сервера'

    def save_to_json(self, data):
        with open(self._currency_data_file, 'a') as file:
            if os.stat(self._currency_data_file).st_size == 0:
                json.dump([data], file)
            else:
                with open(self._currency_data_file) as json_file:
                    data_file = json.load(json_file)
                    data_file.append(data)
                with open(self._currency_data_file, 'w') as json_file:
                    json.dump(data_file, json_file)

    @property
    def get_show(self):
        return f'Курс {self.from_currency} к {self.to_currency}: {self._result[self.to_currency]:.2f}'
