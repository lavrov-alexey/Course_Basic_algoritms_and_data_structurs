""" 2. Написать программу сложения и умножения двух шестнадцатиричных чисел.
При этом каждое число представляется как массив, элементы которого это цифры
числа.
Например, пользователь ввёл A2 и C4F. Сохранить их как [‘A’, ‘2’] и
[‘C’, ‘4’, ‘F’] соответственно.
Сумма чисел из примера: [‘C’, ‘F’, ‘1’], произведение -
[‘7’, ‘C’, ‘9’, ‘F’, ‘E’].

Подсказка: Для решения задачи обязательно примените какую-нибудь коллекцию из
модуля collections
Для лучшего освоения материала можете даже сделать несколько решений этого
задания, применив несколько коллекций из модуля collections
Также попробуйте решить задачу вообще без collections и применить только ваши
знания по ООП (в частности по перегрузке методов)
__mul__ и __add__

Пример:
Например, пользователь ввёл A2 и C4F.
Сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно.
Сумма чисел из примера: [‘C’, ‘F’, ‘1’]
Произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].

1. вариант
defaultdict(list)
int(, 16)
reduce

2. вариант
class HexNumber:
    __add__
    __mul__

hx = HexNumber
hx + hx
hex()"""

from collections import deque
from functools import reduce

def inp_hex_num():
    """Ввод и верификация 16-ричного числа. Результат - список символов"""
    HEX_SET = '0123456789ABCDEF'
    hex_num = input('Введите 16-ричное число (регистр символов A-F '
                    '- не важен): ').upper()
    for char in hex_num:
        try:
            if char not in HEX_SET:
                raise ValueError
        except ValueError:
            print('Введенны символы, не соответствующие 16-ричному числу '
                  '(0-9, A-F/a-f)!')
            exit(1)
    return list(hex_num)


def hex_add(hex_nums):
    """Складывает 16-ричные числа, переданные в деке"""
    sum_dec = sum(int(''.join(hex_num), 16) for hex_num in hex_nums)
    return list(f'{sum_dec:X}')


def hex_mul(hex_nums):
    """Умножает 16-ричные числа, переданые в деке"""
    mul_dec = reduce(lambda hex_one, hex_two: hex_one * hex_two,
                     (int(''.join(hex_num), 16) for hex_num in hex_nums))
    return list(f'{mul_dec:X}')


class HexNum:
    """Класс реализует работу с 16-ричными числами (пока только + и *)"""

    def __init__(self, hex_str):
        # валидация переданных данных на соответствие 16-ричному числу
        HEX_SET = '0123456789ABCDEF'
        for hex_char in hex_str:
            try:
                if hex_char not in HEX_SET:
                    raise ValueError
            except ValueError:
                print('Введенны символы, не соответствующие 16-ричному числу '
                      '(0-9, A-F/a-f)!')
                exit(1)
        # если валидация успешна - сохраняем число в атрибут
        self.hex_num = hex_str

    def __add__(self, other):
        sum_dec = int(''.join(self.hex_num), 16) \
                  + int(''.join(other.hex_num), 16)
        return list(f'{sum_dec:X}')

    def __mul__(self, other):
        mul_dec = int(''.join(self.hex_num), 16) \
                  * int(''.join(other.hex_num), 16)
        return list(f'{mul_dec:X}')


if __name__ == '__main__':

    CNT_HEX_NUM = 2

    print('\nСкрипт осуществляет сложение и умножение 2х 16-ричных чисел\n')

    # Вариант 1 - с использованием deque и функций
    # набираем в дек наши 16-ричные числа в виде списка символов (по ТЗ)
    hex_nums = deque((inp_hex_num() for _ in range(CNT_HEX_NUM)))
    # print(f'{hex_nums=}, {hex_nums[0]=}, {hex_nums[1]=}')
    print('Вариант 1. Реализация через collections.deque')
    print(f'Сумма 16-ричных чисел: {hex_add(hex_nums)}')
    print(f'Произведение 16-ричных чисел: {hex_mul(hex_nums)}')

    # Вариант 2 - с использованием ООП
    hex_one = HexNum(inp_hex_num())
    hex_two = HexNum(inp_hex_num())
    print('\nВариант 2. Реализация через ООП')
    print(f'Сумма 16-ричных чисел: {hex_one + hex_two}')
    print(f'Произведение 16-ричных чисел: {hex_one * hex_two}')
