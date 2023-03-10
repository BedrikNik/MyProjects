import requests
import json
from Список_валют import currency, url_get


class APIException(Exception):
    pass


class BotExtensions:

    @staticmethod
    def get_token():

        with open('data\Token') as t:
            return (t.read())

    @staticmethod
    def get_values():

        reply = "Доступные валюты (допускается ввод в произвольном регистре):\n"
        for k in currency.values():
            reply += '\n' + '\t' + ' - '.join(k)

        return (reply)

    @staticmethod
    def process_data(values: str):

        extxt = f'\nВведите команду в следующем формате:\n ' \
                f'<имя валюты цену которой нужно узнать> <имя валюты в которой надо узнать цену> <количество первой валюты> (например USD RUB 100)\n' \
                f'Допускается не указывать количество (например USD RUB)\n\n' \
                f'список доступных валют можно узнать по команде /values'

        values = values.split()

        if len(values) < 2:
            raise APIException(f'"Параметров должно быть не менее двух"\n'
                               f'Например USD EUR')
        elif len(values) > 3:
            raise APIException(f'"Параметров слишком много"' + extxt)

        elif len(values) == 2:
            values += '1'

        quote, base, amount = values

        quote_r, base_r = '', ''

        for k, v in currency.items():

            if quote.upper() in v:
                quote_r = k

            if base.upper() in v:
                base_r = k

        if quote_r == '':
            raise APIException(f'"Не удалось обработать валюту {quote}"' + extxt)

        if base_r == '':
            raise APIException(f'"Не удалось обработать валюту {base}"' + extxt)

        if quote_r == base_r:
            raise APIException(f'"Введены одинаковые валюты {quote} {base}"' + extxt)

        try:
            amount = abs(float(amount.replace(',', '.')))

        except:
            raise APIException(f'"Не удалось обработать количество {amount}"' + extxt)

        total = BotExtensions.get_price(quote_r, base_r, amount)

        reply = f'{amount} {quote} = {round(total, 9)} {base}'

        return reply

    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        try:
            req = requests.get(url_get[0] + quote + url_get[1] + base)

        except:
            raise Exception(f'"Сервер не отвечает"\n'
                            f'Попробуйте повторить запрос позже.\n')

        try:
            total = json.loads(req.content)[base] * amount

        except:
            raise Exception(f'"Неожиданный ответа сервера: {json.loads(req.content)}"\n'
                            f'Попробуйте повторить запрос позже.\n')

        return total
