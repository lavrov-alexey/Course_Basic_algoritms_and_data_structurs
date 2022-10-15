""" Задание 1.
Приведен код, который позволяет сохранить в массиве индексы четных элементов
другого массива

Сделайте замеры времени выполнения кода с помощью модуля timeit
Оптимизируйте, чтобы снизить время выполнения Проведите повторные замеры.

Добавьте аналитику: что вы сделали и почему!!!
Без аналитики задание не принимается

И прошу вас обратить внимание, что то, что часто ошибочно называют генераторами
списков, на самом деле к генераторам отношения не имеет.
Это называется "списковое включение" - list comprehension."""

from timeit import timeit
from random import randrange


def func_1(nums):
    new_arr = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            new_arr.append(i)
    return new_arr


def func_1_v2(nums):
    return [idx for idx, el in enumerate(nums) if not el % 2]


if __name__ == '__main__':
    CNT_RUNS = 1000                 # кол-во запусков скрипта для замеров
    CNT_ELEMS = 100000                # кол-во эл-тов в массиве для тестов
    MIN_ELEM, MAX_ELEM = 0, 1000    # мин. и макс. значение эл-та массива

    # создаем для тестов массив из 1000 случайных целых чисел
    nums = [randrange(0, 1000) for _ in range(CNT_ELEMS)]

    print('\nСкрипт возвращающий список индексов четных элементов переданного '
          'на вход списка.')
    print(f'Исходный массив ({CNT_RUNS}-элементов): '
          f'{nums[:5]} ... {nums[-5:]}\n')

    time_v1 = timeit('func_1(nums)', setup='from __main__ import func_1, '
                                           'nums', number=CNT_RUNS)
    print(f'Замер {CNT_RUNS}-запусков скрипта вар.1 (исходный): '
          f'{time_v1:.4f} сек.')

    time_v2 = timeit('func_1_v2(nums)', setup='from __main__ import func_1_v2, '
                                              'nums', number=CNT_RUNS)
    print(f'Замер {CNT_RUNS}-запусков скрипта вар.2 (через lc): '
          f'{time_v2:.4f} сек.')

    if time_v2 > time_v1:
        print(f'Исходный вариант быстрее на '
              f'{(time_v2 / time_v1 - 1) * 100:.2f}%')
    else:
        print(f'Вариант через lc быстрее на '
              f'{(time_v1 / time_v2 - 1) * 100:.2f}%')

    # тестовый вывод
    # print(nums)
    # f1, f2 = func_1(nums), func_1_v2(nums)
    # print(f'{len(f1)=}, {f1[:15]=}')
    # print(f'{len(f2)=}, {f2[:15]=}')

"""
Вариант с lc оказался быстрее примерно на 50% (при этом еще и лаконичнее в 
записи и "прозрачнее" для чтения), похоже в связи с тем, что используется 
встроенный функционал lc, более оптимизированный по скорости работы. 
В цикле явным образом создаются промежуточные объекты, выполняются доп. 
выражения.
"""
