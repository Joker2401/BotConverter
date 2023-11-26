import telebot
from config import keys, TOKEN
from classes import ConvertionException, ValueConverted
from telebot import types
bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_start = types.KeyboardButton('/start')
btn_help = types.KeyboardButton('/help')
btn_values = types.KeyboardButton('/values')
markup.add(btn_start, btn_help, btn_values)
@bot.message_handler(commands=['start'])
def start_(message: telebot.types.Message):
    text = ('Чтобы узнать как работать с ботом нажмите на кнопку [/help]')
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    text = ('Для того, чтобы совершить перевод валюты отправьте сообщение по данному шаблону\n'
            '<имя валюты, цену которой хотите узнать>'
            ' <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n'
            'Для того, чтобы узнать доступные для перевода валюты нажмите на кнопку [/values]')
    bot.reply_to(message, text)

#обработчик доступной валюты
@bot.message_handler(commands=['values'])
def avialable_currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

#основная задача бота
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')  # разделяем полученный текст на список по пробелам
    try:
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')
        # quote, base, amount = values
        total_base = ValueConverted.convert(*values)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        # text = f'цена {amount} {quote} в {base} - {total_base}'
        # bot.send_message(message.chat.id, total_base)
        bot.reply_to(message, total_base)


bot.polling()
