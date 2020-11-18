from datetime import timedelta
from .decorators import with_connection

SQL_CREATE_NEW_PAYMENT = 'INSERT INTO bookkeeping (name_payment, cost_payment, quantity, created) VALUES (?, ?, ?, ?)'
SQL_UPDATE_PAYMENT = 'UPDATE bookkeeping SET name_payment=?, cost_payment=?, quantity=? , created =? WHERE id=?'
SQL_SELECT_ALL_PAYMENTS = 'SELECT id, name_payment, cost_payment, quantity, created FROM bookkeeping'
SQL_SELECT_PAYMENT_BY_PK = f'{SQL_SELECT_ALL_PAYMENTS} WHERE id=?'
SQL_SELECT_PAYMENTS_PER_DATE = f'{SQL_SELECT_ALL_PAYMENTS} WHERE created BETWEEN ? AND ?'
SQL_SELECT_PAYMENT_TOP = f'{SQL_SELECT_ALL_PAYMENTS} ORDER BY (cost_payment*quantity) DESC LIMIT 4'


@with_connection()
def initialize(conn, creation_schema):
    with open(creation_schema) as f:
        conn.executescript(f.read())

@with_connection()
def create_payment(conn, name_payment, cost_payment, quantity, created):
    conn.execute(SQL_CREATE_NEW_PAYMENT,(name_payment, cost_payment, quantity, created))

@with_connection()
def update_payment(conn, pk, name_payment, cost_payment, quantity, created):
    conn.execute(SQL_UPDATE_PAYMENT,(name_payment, cost_payment, quantity, created, pk))

@with_connection()
def get_payment(conn, pk):
    cursor = conn.execute(SQL_SELECT_PAYMENT_BY_PK, (pk,))
    return cursor.fetchone()


@with_connection()
def get_payments_per_date(conn, dt, dt_end):
    #dt_end = dt + timedelta(hours=23, minutes=59, seconds=59)
    cursor = conn.execute(SQL_SELECT_PAYMENTS_PER_DATE, (dt, dt_end))
    return cursor.fetchall()


@with_connection()
def get_all_payments(conn):
    return conn.execute(SQL_SELECT_ALL_PAYMENTS).fetchall()

@with_connection()
def get_top_payments(conn):
    return conn.execute(SQL_SELECT_PAYMENT_TOP).fetchall()
