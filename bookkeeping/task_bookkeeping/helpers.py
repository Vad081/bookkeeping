from datetime import datetime
import os

import appdirs
from prettytable import PrettyTable

__all__ = (
    'prompt',
    'input_date',
    'input_datetime',
    'print_table',
    'print_task',
    'user_config_dir',
    'user_data_dir',

)



def prompt(msg, default=None, type_cast=None):
    """ type_cast -> callback """
    while 1:
        value = input(f'{msg}: ')

        if not value:
            return default

        if type_cast is None:
            return value

        try:
            # int('123')
            return type_cast(value)
        except ValueError as err:
            print(err)


def input_int(msg='Введи число', default=None):
    return prompt(msg, default, type_cast=int)

def input_float(msg='Введи число', default=None):
    return prompt(msg, default, type_cast=float)


def input_datetime(msg='Введите дату', default=None,ftm='%Y-%m-%d %H:%M:%S'):
    return prompt(msg,default,lambda v: datetime.strptime(v, ftm))


def input_date(msg='Введите дату', default=None,ftm='%Y-%m-%d'):
    value = input_datetime(msg, default, ftm)

    if value is None:
        return default

    return value.date() if isinstance(value,datetime) else value

def print_table(headers, iterable):
    table = PrettyTable(headers)

    for row in iterable:
        table.add_row(row)

    print(table)

def print_payment():
    print(dedent(f'''
    ----------------------------------------------------------------
                Платеж: "{payment['name_payment']}"
             Стоимость: {payment['cost_apyment']}
            Количество: {payment['quantity']}
                Создан: {payment['created']:%d.%m.%Y в %H:%M}
    ----------------------------------------------------------------

    ----------------------------------------------------------------
    '''))



def make_dirs_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path,0o755)
    return path


user_config_dir = make_dirs_if_not_exists(appdirs.user_config_dir(__package__))
user_data_dir = make_dirs_if_not_exists(appdirs.user_data_dir(__package__))
