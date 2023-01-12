import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username}!\n\n'
                                      f'• Этот бот умеет конвертировать валюты. Чтобы попробовать, введи команду в'
                                      f' формате:\n'
                                      f'<b>что_перевести</b>(пробел)<b>во_что_перевести</b>(пробел)'
                                      f'<b>сколько_перевести</b>\n\n'
                                      f'• Названия валют для <i>"что_перевести"</i> и <i>"во_что_перевести"</i> пиши'
                                      f' в форме единственного числа именительного падежа.\n'
                                      f'• И с маленькой буквы.\n'
                                      f'• Если количество валюты — не целое число, используй <i>точку</i> для отделения'
                                      f' дробной части.\n\n'
                                      f'• Посмотреть список всех доступных валют: /values\n(в общем, писать валюты '
                                      f'нужно так, как они указаны в /values)\n'
                                      f'• Вызвать справку по оформлению команды: /help\n'
                                      f'• Запустить бот: /start\n'
                                      f'• Комментарий создателя бота: /comment')


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '<b>• Как вводить команду? •</b>\n\n' \
           '<b>что_перевести</b>(пробел)<b>во_что_перевести</b>(пробел)<b>сколько_перевести</b>\n' \
           'Например: <i>рубль евро 85700</i>\n\n' \
           '<b>• Дополнительные правила ввода •</b>\n\n' \
           '1. Названия валют для <i>"что_перевести"</i> и <i>"во_что_перевести"</i> пиши в форме единственного числа' \
           ' именительного падежа.\n' \
           '2. И с маленькой буквы.\n' \
           '3. Если количество валюты — не целое число, используй <i>точку</i> для отделения дробной части.\n\n' \
           '• Посмотреть список всех доступных валют: /values\n(в общем, писать валюты ' \
           'нужно так, как они указаны в /values)\n' \
           '• Вызвать эту справку: /help (в ней ничего не изменится 🙃)\n' \
           '• Запустить бот: /start\n' \
           '• Комментарий создателя бота: /comment'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n• '.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['comment'])
def comment(message: telebot.types.Message):
    text = '"Итоговый проект по ООП", суть которого — перепечатать код из видео и заменить в нём несколько слов — ' \
           'это, конечно, сильно. Но спасибо, что с этой домашкой можно было не заморачиваться 🙊\n' \
           'Буду рада узнать, что был какой-то подвох, который я не заметила, и задание на самом деле сложнее)'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не то количество параметров. Возможно, ты ввёл лишний пробел или нарушил '
                               'формат ввода:\n'
                               '<b>что_перевести</b>(пробел)<b>во_что_перевести</b>(пробел)<b>сколько_перевести</b>')

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f"Цена {amount} {base} в {quote} — {'{:0.4f}'.format(total_base)}"
        # Используется форматирование, чтобы при вводе очень больших чисел пользователь видел число в привычном, а не в
        # экспоненциальном представлении. Чем бы ни тешился, лишь бы не возмущался, что бот ему что-то не то выдаёт.
        # При этом при конвертации очень маленьких значений из-за округления пользователь может получить результат
        # "0.0000", хотя где-то дальше и будут значащие цифры - но этот ноль по сути всё равно будет правдой. Поэтому
        # пусть остаётся так, пока я не придумала, как сделать лучше :)
        bot.send_message(message.chat.id, text)


bot.polling()
