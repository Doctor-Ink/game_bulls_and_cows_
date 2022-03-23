import random

def get_digit():
    lst = [1,2,3,4,5,6,7,8,9,0]
    number = []
    for _ in range(4):
        num = random.choice(lst)
        number.append(num)
        lst.remove(num)
    return number

def check_input(num):
    if num.isdigit() and len(num) == 4 and len(num) == len(set(num)):
        return num
    else:
        print('Некорректный ввод')

def cow_bull(attempt, number):
    cow = 0
    bull = 0
    for i in attempt:
        if i in number and attempt.index(i) == number.index(i):
            bull +=1
        elif i in number:
            cow +=1
    print('> быки -', bull, 'коровы - ', cow)




