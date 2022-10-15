""" Задача 4.
Поработайте с обычным словарем и OrderedDict.
Выполните операции с каждым их них (заполнение, получение элемента) и сделайте
замеры. Опишите полученные результаты, сделайте выводы.
И есть ли смысл исп-ть OrderedDict в Python 3.6 и более поздних версиях?"""

from collections import OrderedDict
from timeit import timeit
from random import randint

CNT_RUNS = 5000      # кол-во запусков скрипта для замеров
CNT_ELEMS = 1000     # кол-во эл-тов в массиве для тестов


def fill_dct(cnt_els=CNT_ELEMS):
    """Возвращает словарь, заполненный cnt_els последовательными цифрами"""
    return {f'{num}': f'{num}' for num in range(cnt_els)}


def fill_ord_dct(cnt_els=CNT_ELEMS):
    """Возвращает упорядоченный словарь, заполненный cnt_els последовательными
    цифрами"""
    return OrderedDict((f'{num}', f'{num}') for num in range(cnt_els))


if __name__ == '__main__':

    # замеры заполнения элементами
    time_dct = timeit('fill_dct(CNT_ELEMS)',
                      setup='from __main__ import fill_dct, CNT_ELEMS',
                      number=CNT_RUNS)
    time_ord_dct = timeit('fill_ord_dct(CNT_ELEMS)',
                      setup='from __main__ import fill_ord_dct, CNT_ELEMS',
                      number=CNT_RUNS)
    print(f'{CNT_RUNS:,d}-запусков скрипта заполнения {CNT_ELEMS:,d}-эл-ми:\n'
          f'\t- dict: {time_dct:.5f} сек.\n '
          f'\t- ord_dict: {time_ord_dct:.5f} сек.')

    if time_ord_dct > time_dct:
        print(f'dict выполняется быстрее на '
              f'{(time_ord_dct / time_dct - 1) * 100:,.2f}%')
    else:
        print(f'ord_dict выполняется быстрее на '
              f'{(time_dct / time_ord_dct - 1) * 100:,.2f}%')

    # замеры получения элемента
    tst_dct = fill_dct(CNT_ELEMS)
    tst_ord_dct = fill_ord_dct(CNT_ELEMS)
    tst_dct[f'{randint(0, CNT_ELEMS)}']

    time_dct = timeit("tst_dct[f'{randint(0, CNT_ELEMS - 1)}']",
                      setup='from __main__ import tst_dct, CNT_ELEMS, randint',
                      number=CNT_RUNS)
    time_ord_dct = timeit("tst_ord_dct[f'{randint(0, CNT_ELEMS - 1)}']",
                      setup='from __main__ import tst_ord_dct, CNT_ELEMS, '
                            'randint',
                      number=CNT_RUNS)
    print(f'{CNT_RUNS:,d}-запусков скрипта получения элемента:\n'
          f'\t- dict: {time_dct:.5f} сек.\n '
          f'\t- ord_dict: {time_ord_dct:.5f} сек.')

    if time_ord_dct > time_dct:
        print(f'dict выполняется быстрее на '
              f'{(time_ord_dct / time_dct - 1) * 100:,.2f}%')
    else:
        print(f'ord_dict выполняется быстрее на '
              f'{(time_dct / time_ord_dct - 1) * 100:,.2f}%')

"""
Выводы:
Учитывая, что начиная с Python v.3.6 в обычных словарях уже гарантируется 
сохранения порядка добавления элементов, и скорость добавления элементов (как 
видно по замерам) у стандартного словаря выше примерно на 50%, а получение 
элементов - по времени одинаково, то в использовании OrderedDict особого 
смысла уже нет, если только нет специфических потребностей в уникальных 
методах OrderedDict.
"""
