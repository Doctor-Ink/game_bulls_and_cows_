# -*- coding: utf-8 -*-
from engine import check_input, get_digit, cow_bull

print('------Компьютер загадал число')
number = get_digit()
step = 0
while True:
    attempt = input('Введите четырёхзначное число с неповторяющимися цифрами - ')
    if check_input(num=attempt):
        cow_bull(attempt=attempt, number=number)
        step += 1
        if attempt == number:
            print(f'Вы угадали!!! Количество ходов - {step}')
            print('Хотите ещё партию?')
            enter = input('Введите 1 для новой партии, 0 - для выхода  ')
            if enter == '1':
                print('------Компьютер загадал число')
                number = get_digit()
                step = 0
            else:
                break
    else:
        step +=1
