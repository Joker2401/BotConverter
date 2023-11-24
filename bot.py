import json

import requests
import telebot

TOKEN = '6919917762:AAGPbb2AKL7WhKKvHqsZxlpBBPqjGzR2hjc'
bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'биткоин': 'BTC'
}


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
    quote, base, amount = message.text.split(' ') #разделяем полученный текст на список по пробелам
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)
bot.polling()