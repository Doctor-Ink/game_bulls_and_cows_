from random import choice


def get_digit():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    number = []
    for _ in range(4):
        num = choice(lst)
        number.append(num)
        lst.remove(num)
    return ''.join(str(_) for _ in number)


def check_input(num):
    if num.isdigit() and len(num) == 4 and len(num) == len(set(num)):
        return int(num)
    else:
        print('Некорректный ввод')


def cow_bull(cur_num, res_number):
    cow = 0
    bull = 0
    for i in cur_num:
        if i in res_number and cur_num.index(i) == res_number.index(i):
            bull += 1
        elif i in res_number:
            cow += 1
    return bull, cow

