from collections import OrderedDict, namedtuple
from datetime import datetime, timedelta, date
import pkg_resources
from textwrap import dedent
import sys


from . import helpers as h
from . import storage
from .services import make_connection


Action = namedtuple('Action',('func','title'))
actions = OrderedDict()


def action(cmd, title):
    def decorator(func):
        actions[str(cmd)] = Action(func, title)
        return func
    return decorator

def input_payment():
    payment_id = h.input_int('Введите ID платежа')
    payment = storage.get_payment(payment_id)
    if payment is None:
        print(f'Платеж с ID {payment_id} не найдена.')

    return payment


def input_payment_data(payment=None):
    """Ввод данных о платеже"""
    payment = dict(payment) if payment is not None else {}
    data = {}

    data['name_payment'] = h.prompt(
        'Название', default=payment.get('name_payment')
    )

    data['cost_payment'] = h.input_float('Стоимость', default=payment.get('cost_payment'))


    data['quantity'] = h.input_int('Количество', default=1)

    data['created'] = h.input_datetime('Время платежа',default=payment.get('created',datetime.now()))

    return data



def display_all_data(payment=None):
    """Печатает все данные о платежах из БД."""
    print(f'{payment["id"]},{payment["name_payment"]}, {payment["cost_payment"]},{payment["quantity"]},{payment["created"]}')

@action(1, 'Добавить платеж')
def add_payment(payment=None):
    """Добавить платеж"""
    data = input_payment_data()
    storage.create_payment(**data)

    print(f'Платеж "{data["name_payment"]}" успешно создан.')

@action(2, 'Отредактировать платеж')
def edit_payment():
    """Отредактировать платеж"""
    payment = input_payment()

    if payment is not None:
        data = input_payment_data(payment)
        storage.update_payment(payment['id'], **data)
        print(f'Платеж "{payment["name_payment"]}" успешно отредактирован.')


@action(3, 'Вывести все платежи за указанный период')
def period_payment():
    """Вывести все платежи за указанный период"""
    start = h.input_datetime('Начало периода')
    end = h.input_datetime('Конец периода')
    payments = storage.get_payments_per_date(start,end)
    h.print_table(['ID', 'Название', 'Стоимость','Количество', 'Дата'],payments)
    for payment in payments:
        display_all_data(payment)




@action(4, 'Вывести топ самых крупных платежей')
def top_payment():
    """Вывести топ самых крупных платежей"""
    payments = storage.get_top_payments()
    h.print_table(['ID', 'Название', 'Стоимость','Количество', 'Дата'],payments)
    for payment in payments:
        display_all_data(payment)






@action('m', 'Показать меню')
def action_show_menu():
    """Показать меню"""
    for cmd,action in actions.items():
        print(f'{cmd}. {action.title}')

@action('q', 'Выйти')
def action_exit():
    """Выйти"""
    sys.exit(0)





def main():
    schema_path = pkg_resources.resource_filename(__package__, 'resources/schema.sql')
    storage.initialize(schema_path)

    action_show_menu()

    while 1:
        cmd = input('\nВведите команду: ').strip()
        action = actions.get(cmd)

        if action:
            action.func()
        else:
            print('Вы ввели не верную команду')
