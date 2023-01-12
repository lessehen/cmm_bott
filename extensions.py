import requests
import json
from config import keys


class APIException(Exception):
    pass


'''
Что происходит дальше, цитирую задание:
"Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента: 
1. имя валюты, цену на которую надо узнать, — base, (что переводим)
2. имя валюты, цену в которой надо узнать, — quote, (во что переводим)
3. количество переводимой валюты — amount 
и возвращает нужную сумму в валюте".
Если правильно расшифровала придаточные предложения, нужно поменять местами quote и base из кода, данного в скринкасте ☻
'''


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Зачем переводить {base} в {quote}? Получится {amount}, но это понятно и без меня. '
                               f'Попробуй по-другому :)')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не могу обработать валюту "{base}". Проверь, нет ли в названии ошибок и доступна '
                               f'ли эта валюта в /values.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не могу обработать валюту "{quote}". Проверь, нет ли в названии ошибок и доступна '
                               f'ли эта валюта в /values.')

        if amount == '0':
            raise APIException(f'Ты уверен, что хочешь конвертировать 0 {base}?\n'
                               f'Если да, то будет 0 🙃\n'
                               f'Если нет — введи команду заново.')

        if amount[0] == '0' and '.' not in amount:
            raise APIException(f'Введённое тобой количество начинается с <i>0</i>. Проверь, не пропустил ли ты цифру '
                               f'или точку или введи число <i>{amount}</i> без нулей в начале.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}".\n'
                               f'Правила ввода: /values')

        if amount < 0:
            raise APIException(f'Увы, но конвертировать отрицательные числа я не умею. Попробуй что-нибудь другое.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[keys[quote]])*amount
        # То ли я невнимательно смотрела, то ли в скринкасте забыли умножить курс валюты на amount.

        return total_base
