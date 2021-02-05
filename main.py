import json
import datetime


with open('\sber\operations.json', 'r', encoding='utf-8') as file:
    pars = json.load(file)
    pars = list(filter(lambda x: x.get('id', False), pars))
    pars.sort(key=lambda date: datetime.datetime.strptime(date['date'], "%Y-%m-%dT%H:%M:%S.%f"))

    pars.reverse()

    json_operations = []

    for i in pars:
        if i['state'] == 'EXECUTED':
            json_operations.append(i)
        if len(json_operations) == 5:
            break

    def card(number_card):
        """
        эта функция возвращает номер карты с маской

        """
        return '{0} {1}** **** {2}'.format(number_card[:4], number_card[4:6], number_card[-4:])

    def account(number_score):
        """
        Эта функция возфращает номер счета с маской

        """
        return '**{0}'.format(number_score[-4:])

    def card_or_account(value_list):
        """
        Эта функция определяет вид денежного носителя

        """
        if value_list.count('Счет') != 0:
            number_account = value_list.split()
            return number_account[0] + ' ' + account(number_account[-1])
        else:
            number_card_list = value_list.split()
            number_card = number_card_list.pop()
            return ' '.join(number_card_list) + ' ' + card(number_card)

    for y in json_operations:
        print('{0} {1}'.format(y['date'][:10].replace('-', '.'), y['description']))
        if y.get('from', False):
            print(card_or_account(y['from']), '->',  card_or_account(y['to']))
        else:
            print(card_or_account(y['to']))
        print('{0} {1}'.format(y['operationAmount']['amount'], y['operationAmount']['currency']['name']), end='\n\n')