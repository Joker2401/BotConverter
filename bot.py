import json

import requests
import telebot

TOKEN = '6919917762:AAGPbb2AKL7WhKKvHqsZxlpBBPqjGzR2hjc'
bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'биткоин': 'BTC'
}

class ConvertionException(Exception):
    pass

class ValueConverted:


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
    #биткоин доллар 1
    values = message.text.split(' ') #разделяем полученный текст на список по пробелам
    if len(values) > 3:
        raise ConvertionException('Слишком много параметров')

    quote_ticker, base_ticker = keys[quote], keys[base]
    quote, base, amount = values

    if quote == base: #если переводим одинаковые валюты
        raise ConvertionException('Зачем переводить одинаковые валюты?')

    try: # если пользователь вводит в количество валюты не число
        if amount.isdigit():
            pass
        else:
            raise ConvertionException
    except:
        raise ConvertionException('Введите число!')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {quote}')

    try:
        base_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {base}')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)
bot.polling()