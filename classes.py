import requests
import json
from config import keys
class ConvertionException(Exception):
    pass
class ValueConverted:
    @staticmethod
    def convert(quote, base, amount):
        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote_ticker}')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base_ticker}')

        # quote_ticker, base_ticker = keys[quote], keys[base]
        if quote_ticker == base_ticker:  # если переводим одинаковые валюты
            raise ConvertionException('Зачем переводить одинаковые валюты?')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Не удалось обработать количество')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)
        new_total_base = total_base[base_ticker] * amount
        new_total_base = round(new_total_base, 3)
        message = f'Цена {amount} {quote_ticker} в {base_ticker} - {new_total_base}'
        return message
