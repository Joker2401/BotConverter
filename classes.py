import requests
import json
from config import keys
class ConvertionException(Exception):
    pass
class ValueConverted:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote_ticker, base_ticker = keys[quote], keys[base]
        if quote == base:  # если переводим одинаковые валюты
            raise ConvertionException('Зачем переводить одинаковые валюты?')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote_ticker}')
        try:
            base_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Введите число')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        new_total_base = total_base[base_ticker] * amount
        new_total_base = round(new_total_base, 3)
        mes1 = f'Цена {amount} {quote_ticker} в {base_ticker} - {new_total_base}'
        return mes1
