""" Задача 3.
В соответствии с документацией Python, deque – это обобщение стеков и очередей.
Вот основное правило: если вам нужно что-то быстро дописать или вытащить,
используйте deque. Если вам нужен быстрый случайный доступ, используйте list.

Задача: 
1) создайте простой список (list) и очередь (deque). Сделайте замеры и оцените
что заполняется быстрее.
2) Выполните различные операции с каждым из объектов. Сделайте замеры и оцените,
где и какие операции быстрее.

В первую очередь необходимо выполнить замеры для ф-ций appendleft, popleft,
extendleft дека и для их аналогов у списков."""


from timeit import timeit
from random import randint
from collections import deque
from itertools import islice

CNT_RUNS = 1000       # кол-во запусков скрипта для замеров
CNT_ELEMS = 100000    # кол-во эл-тов в массиве для тестов
CNT_ADD_ELEMS = 100   # кол-во эл-тов для пакетного добавления
MIN_ELEM, MAX_ELEM = 1000, 1000000  # мин. и макс. значение эл-та массива


def fill_lst(nums):
    """Возвращает список из переданного массива элементов"""
    return [num for num in nums]


def fill_deq(nums):
    """Возвращает deque из переданного массива элементов"""
    return deque(nums)


def append_left_lst(tst_lst: list, el):
    # print(f'Был lst {tst_lst[:2]}..., вставили слева {el}', end=', ')
    tst_lst.insert(0, el)
    # print(f'стало {tst_lst[:2]}...')
    return tst_lst


def append_left_deq(tst_deq: deque, el):
    # print(f'Был deque {tst_deq[0]}, {tst_deq[1]}..., вставили слева {el}',
    #       end=', ')
    tst_deq.appendleft(el)
    # print(f'стало {tst_deq[0]}, {tst_deq[1]}...')
    return tst_deq


def pop_left_lst(tst_lst: list):
    # print(f'Был lst {tst_lst[:2]}..., забираем слева {tst_lst[0]}', end=', ')
    left_el = tst_lst.pop(0)
    # print(f'стало {tst_lst[:2]}...')
    return left_el


def pop_left_deq(tst_deq: deque):
    # print(f'Был deque {tst_deq[0]}, {tst_deq[1]}..., забираем слева
    # {tst_deq[0]}', end=', ')
    left_el = tst_deq.popleft()
    # print(f'стало {tst_deq[0]}, {tst_deq[1]}...')
    return left_el


def extend_left_lst(tst_lst: list, els):
    # print(f'Был lst {tst_lst[:2]}..., вставили слева {len(els)} элементов',
    # end=', ')
    for idx, el in enumerate(els):
        tst_lst.insert(idx, el)
    # print(f'стало {tst_lst[:2]}...')
    return tst_lst


def extend_left_deq(tst_deq: deque, els):
    # print(f'Был deque {tst_deq[0]}, {tst_deq[1]}..., вставили слева
    # {len(els)} элементов', end=', ')
    tst_deq.extendleft(els)
    # print(f'стало {tst_deq[0]}, {tst_deq[1]}...')
    return tst_deq


if __name__ == '__main__':

    print('\nСкрипт сравнения list и deque\n')

    # создаем тестовый набор
    nums = tuple(randint(MIN_ELEM, MAX_ELEM) for _ in range(CNT_ELEMS))
    tst_lst = fill_lst(nums)
    tst_deq = fill_deq(nums)
    # тестовый вывод
    # print(f'Исходный tupple: {nums[:2]} ... {nums[-2:]}')
    # print(f'list: {tst_lst[:2]} ... {tst_lst[-2:]}')
    # print(f'deque: {tst_deq[0]}, {tst_deq[1]} ... '
    #       f'{tst_deq[len(tst_deq)-2]}, {tst_deq[len(tst_deq)-1]}')

    # замеры заполнения элементами
    time_lst = timeit('fill_lst(nums)', setup='from __main__ import fill_lst, '
                                              'nums', number=CNT_RUNS)
    time_deq = timeit('fill_deq(nums)', setup='from __main__ import fill_deq, '
                                              'nums', number=CNT_RUNS)
    print(f'{CNT_RUNS:,d}-запусков скрипта заполнения {CNT_ELEMS:,d}-эл-ми:\n'
          f'\t- list: {time_lst:.5f} сек.\n '
          f'\t- deque: {time_deq:.5f} сек.')

    if time_deq > time_lst:
        print(f'list выполняется быстрее на '
              f'{(time_deq / time_lst - 1) * 100:,.2f}%')
    else:
        print(f'deque выполняется быстрее на '
              f'{(time_lst / time_deq - 1) * 100:,.2f}%')

    # замеры по добавлению элемента слева
    add_num = 666666  # добавляемый элемент
    time_lst = timeit('append_left_lst(tst_lst, add_num)',
                      setup='from __main__ import append_left_lst, '
                            'tst_lst, add_num', number=CNT_RUNS)
    time_deq = timeit('append_left_deq(tst_deq, add_num)',
                      setup='from __main__ import append_left_deq, '
                            'tst_deq, add_num', number=CNT_RUNS)
    print(f'\n{CNT_RUNS:,d}-запусков скрипта добавления эл-та слева:\n'
          f'\t- list ({len(tst_lst):,d} элементов): {time_lst:.5f} сек.\n '
          f'\t- deque ({len(tst_deq):,d} элементов): {time_deq:.5f} сек.')

    if time_deq > time_lst:
        print(f'list выполняется быстрее на '
              f'{(time_deq / time_lst - 1) * 100:,.2f}%')
    else:
        print(f'deque выполняется быстрее на '
              f'{(time_lst / time_deq - 1) * 100:,.2f}%')

    # замеры по извлечению элемента слева
    time_lst = timeit('pop_left_lst(tst_lst)',
                      setup='from __main__ import pop_left_lst, tst_lst',
                      number=CNT_RUNS)
    time_deq = timeit('pop_left_deq(tst_deq)',
                      setup='from __main__ import pop_left_deq, tst_deq',
                      number=CNT_RUNS)
    print(f'\n{CNT_RUNS:,d}-запусков скрипта извлечения эл-та слева:\n'
          f'\t- list ({len(tst_lst):,d} элементов): {time_lst:.5f} сек.\n '
          f'\t- deque ({len(tst_deq):,d} элементов): {time_deq:.5f} сек.')

    if time_deq > time_lst:
        print(f'list выполняется быстрее на '
              f'{(time_deq / time_lst - 1) * 100:,.2f}%')
    else:
        print(f'deque выполняется быстрее на '
              f'{(time_lst / time_deq - 1) * 100:,.2f}%')

    # замеры по пакетному добавлению элементов слева
    # генерим элементы для добавления
    add_nums = tuple(randint(MIN_ELEM, MAX_ELEM) for _ in range(CNT_ADD_ELEMS))

    time_lst = timeit('extend_left_lst(tst_lst, add_nums)',
                      setup='from __main__ import extend_left_lst, '
                            'tst_lst, add_nums', number=CNT_RUNS)
    time_deq = timeit('extend_left_deq(tst_deq, add_nums)',
                      setup='from __main__ import extend_left_deq, '
                            'tst_deq, add_nums', number=CNT_RUNS)
    print(f'\n{CNT_RUNS:,d}-запусков скрипта пакетного добавления '
          f'{CNT_ADD_ELEMS} эл-тов слева:\n'
          f'\t- list ({len(tst_lst):,d} элементов): {time_lst:.5f} сек.\n '
          f'\t- deque ({len(tst_deq):,d} элементов): {time_deq:.5f} сек.')

    if time_deq > time_lst:
        print(f'list выполняется быстрее на '
              f'{(time_deq / time_lst - 1) * 100:,.2f}%')
    else:
        print(f'deque выполняется быстрее на '
              f'{(time_lst / time_deq - 1) * 100:,.2f}%')

"""=============================================================================
Выводы
Замеры по функциям конечно копипаста и по-хорошему их нужно было бы оформить 
в виде отдельной функции, либо декоратора, но суть здесь в другом и тратить 
время на это сейчас не вижу необходимости.
Замеры подтверждают известные рекомендации - если нужен быстрый произвольный 
доступ к элементам - лучше пользоваться списками, если нужно часто 
добавлять/убирать элементы по краям - однозначно выбор за deque!
============================================================================ """
