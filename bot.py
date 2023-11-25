import json

import requests
import telebot

TOKEN = '6919917762:AAGPbb2AKL7WhKKvHqsZxlpBBPqjGzR2hjc'
bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'биткоин': 'BTC',
    'рубль': 'RUB'
}

class ConvertionException(Exception):
    pass

class ValueConverted:
    @staticmethod
    def convert(quote: str, base: str, amount: str):




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
        try:  # если пользователь вводит в количество валюты не число
            if amount.isdigit():
                pass
            else:
                raise ConvertionException
        except:
            raise ConvertionException('Введите число!')
        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base

# обработчик команд start help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работать введите боту команду в следующем формате: \n <имя валюты> '
            '<в какую валюту перевести> '
            '<количество валюты> \n'
            'Увидеть список доступных валют /values')
    bot.reply_to(message, text)


#обработчик доступной валюты
@bot.message_handler(commands=['values'])
def avialable_currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

#основная задача бота
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    values = message.text.split(' ')  # разделяем полученный текст на список по пробелам
    if len(values) != 3:
        raise ConvertionException('Слишком много параметров')
    quote, base, amount = values
    total_base = ValueConverted.convert(quote, base, amount)


    text = f'цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)
bot.polling()