import PySimpleGUI as sg
import os
from brownie import accounts, Contract, network
from dotenv import load_dotenv
load_dotenv()
sg.theme('sandy beach')

network.connect('ganache-local')
credit_address = '0x5b0630DDF920A7a91A6eD8B96fdfB22589783e14'
bank_address = '0xB6DEBA730C1Dd36E11cd7dB243f1727533828D0e'
credit_contract = Contract(credit_address)
bank_contract = Contract(bank_address)

account = accounts.add(os.getenv("PRIVATE_KEY"))
account1 = accounts.add(os.getenv("PRIVATE_KEY1"))
account2 = accounts.add(os.getenv("PRIVATE_KEY2"))

def find_client(login):
    cl = bank_contract.getClients()
    client = None
    for c in cl:
        if c[1] == login:
            client = c
            break
    return client

def main_window(acc):
    layout_main = [
        [sg.Text(f'Ваш баланс: {credit_contract.balanceOf(acc)} CRT', key='-MAIN-BALANCE-')],
        [sg.Button('Взять кредит'), sg.Push(), sg.Button('Вернуть кредит')],
        [sg.Push(), sg.Button('Выйти')]
    ]
    return sg.Window('CreditToken Bank. Главная', layout_main)

def take_credit_window():
    layout_take_credit = [
        [sg.Push(), sg.Text('Введите сумму:'), sg.Push()],
        [sg.Push(), sg.InputText(key='-CREDIT-SUM-'), sg.Push()],
        [sg.Push(), sg.Text('Введите количество месяцев:'), sg.Push()],
        [sg.Push(), sg.InputText(key='-CREDIT-MONTH-'), sg.Push()],
        [sg.Push(), sg.Button('Рассчитать сумму'), sg.Push()],
        [sg.Push(), sg.Text('Общая сумма кредита составит:', key='-TOTAL-CREDIT-'), sg.Push()],
        [sg.Push(), sg.Text('Ежемесячный платеж составит:', key='-TOTAL-MONTH-'), sg.Push()],
        [sg.Push(), sg.Button('Взять кредит'), sg.Push()],
        [sg.Push(), sg.Button('Выйти')]
    ]
    return sg.Window('CreditToken Bank. Взять кредит', layout_take_credit)

def return_credit_window(acc, login):
    client = find_client(login)
    layout_return_credit = [
        [sg.Text(f'Ваш баланс: {credit_contract.balanceOf(acc)} CRT', key='-RETURN-BALANCE-')],
        [sg.Text(f'Сумма к погашению: {client[4][2]} CRT', key='-RETURN-SUM-')],
        [sg.Push(), sg.Text('Введите сумму платежа:'), sg.Push()],
        [sg.Push(), sg.InputText(key='-CREDIT-MONTH-'), sg.Push()],
        [sg.Push(), sg.Button('Внести платеж'), sg.Push()],
        [sg.Push(), sg.Button('Выйти')]
    ]
    return sg.Window('CreditToken Bank. Вернуть кредит', layout_return_credit)

users_db = [
    ('acc0', 'acc0'),
    ('acc1', 'acc1'),
    ('acc2', 'acc2')
]

layout = [
    [sg.Text('Пожалуйста, выполните вход')],
    [sg.Push(), sg.Text('Логин:'), sg.InputText(key='-LOGIN-', do_not_clear=False)],
    [sg.Push(), sg.Text('Пароль:'), sg.InputText(
        key='-PASS-', password_char='*', do_not_clear=False)],
    [sg.Push(), sg.Button('Войти'), sg.Push()],
    [sg.Push(), sg.Button('Выход')]
]

window = sg.Window('CreditToken Bank. Вход', layout)

while True:
    event, values = window.read()  # отслеживание состояния и переменных главного окна

    # обработка события выхода из приложения
    if event == sg.WINDOW_CLOSED or event == 'Выход':
        break

    # обработка события нажатия на кнопку "Войти"
    if event == 'Войти' and (values['-LOGIN-'], values['-PASS-']) in users_db:
        acc_to_use = None
        login = values['-LOGIN-']
        pwd = values['-PASS-']
        if values['-LOGIN-'] == 'acc0':
            acc_to_use = account
        if values['-LOGIN-'] == 'acc1':
            acc_to_use = account1
        if values['-LOGIN-'] == 'acc2':
            acc_to_use = account2

        window_main = main_window(acc_to_use)
        while True:
            event_m, values_m = window_main.read()
            if event_m == sg.WINDOW_CLOSED or event_m == 'Выйти':
                break

            if event_m == 'Взять кредит':
                window_take_credit = take_credit_window()
                while True:
                    event_t, values_t = window_take_credit.read()
                    if event_t == sg.WINDOW_CLOSED or event_t == 'Выйти':
                        break
                    if event_t == 'Рассчитать сумму':
                        s = int(values_t['-CREDIT-SUM-'])
                        m = int(values_t['-CREDIT-MONTH-'])
                        sum_credit = bank_contract.calculateTotalSum(s, m)
                        window_take_credit['-TOTAL-CREDIT-'].update(f'Общая сумма кредита составит: {sum_credit} CRT')
                    if event_t == 'Взять кредит':
                        try:
                            s = int(values_t['-CREDIT-SUM-'])
                            m = int(values_t['-CREDIT-MONTH-'])
                            sum_credit = bank_contract.calculateTotalSum(s, m)
                            credit_contract.approve(bank_address, sum_credit, {'from': acc_to_use})
                            bank_contract.takeCredit(login, pwd, s, m, {'from': acc_to_use})
                            sg.Popup('Успешно оформили кредит', title='Успех')
                            window_main['-MAIN-BALANCE-'].update(f'Ваш баланс: {credit_contract.balanceOf(acc_to_use)} CRT')
                        except:
                            sg.Popup('Не получилось оформить кредит', title='Ошибка')
                    
                window_take_credit.close()

            if event_m == 'Вернуть кредит':
                window_return_credit = return_credit_window(acc_to_use, login)
                while True:
                    event_r, values_r = window_return_credit.read()
                    if event_r == sg.WINDOW_CLOSED or event_r == 'Выйти':
                        break
                    if event_r == 'Внести платеж':
                        try:
                            pay = int(values_r['-CREDIT-MONTH-'])
                            bank_contract.returnCredit(pay, {'from': acc_to_use})
                            sg.Popup('Успешно внесен платеж', title='Успех')
                            window_main['-MAIN-BALANCE-'].update(f'Ваш баланс: {credit_contract.balanceOf(acc_to_use)} CRT')
                            window_return_credit['-RETURN-BALANCE-'].update(f'Ваш баланс: {credit_contract.balanceOf(acc_to_use)} CRT')
                            cl = find_client(login)
                            window_return_credit['-RETURN-SUM-'].update(f'Сумма к погашению: {cl[4][2]} CRT')
                        except:
                            sg.Popup('Не получилось внести платеж', title='Ошибка')

                window_return_credit.close()


        window_main.close()

    if event == 'Войти' and (values['-LOGIN-'], values['-PASS-']) not in users_db:
        sg.Popup('Ошибка. Проверьте введенные данные', title='Ошибка')
    
window.close()