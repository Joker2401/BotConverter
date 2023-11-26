import telebot
from config import keys, TOKEN
from classes import ConvertionException, ValueConverted
bot = telebot.TeleBot(TOKEN)
# обработчик команд start help
@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
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
