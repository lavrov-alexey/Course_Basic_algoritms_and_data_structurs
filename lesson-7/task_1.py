from random import randint
from timeit import default_timer

"""1. Отсортируйте по убыванию методом "пузырька" одномерный целочисленный
массив, заданный случайными числами на промежутке [-100; 100).
Выведите на экран исходный и отсортированный массивы.
Сортировка должна быть реализована в виде функции.

Обязательно доработайте алгоритм (сделайте его умнее).
Идея доработки: если за проход по списку не совершается ни одной сортировки,
то завершение. Обязательно сделайте замеры времени обеих реализаций и укажите
дала ли оптимизация эффективность.

Подсказка: обратите внимание, сортируем не по возрастанию, как в примере,
а по убыванию.

Сделайте выводы!!!
Опишите в чем была ваша доработка и помогла ли вам доработка??"""

"""
Итоги. Даная оптимизация показывает свою эффективность только при подаче на вход
функции отсортированного массива, при случайных или близким к ним значениям  
массива - замеры показывают улучшение в пределах погрешности измерений 
(менее 1%). Значимого смысла данная оптимизация не несет.
"""


def buble_sort_v1(arr, sort_incr=True):
    """
    Возвращает отсортированный методом "пузырька" переданный массив arr
    :param arr: массив для сортировки
    :param sort_incr: True - сортировка по возрастанию, False - по убыванию
    :return: отсортированный массив
    """
    for _ in range(len(arr) - 1):
        for idx in range(len(arr) - 1):
            curr_item, next_item = arr[idx], arr[idx + 1]
            if curr_item > next_item and sort_incr\
                    or curr_item < next_item and not sort_incr:
                arr[idx], arr[idx + 1] = next_item, curr_item
    return arr


def buble_sort_v2(arr, sort_incr=True):
    """
    Возвращает отсортированный методом "пузырька" переданный массив arr
    с добавлением контроля хотя бы 1 перестановки
    :param arr: массив для сортировки
    :param sort_incr: True - сортировка по возрастанию, False - по убыванию
    :return: отсортированный массив
    """
    for _ in range(len(arr) - 1):
        is_not_changed = True
        for idx in range(len(arr) - 1):
            curr_item, next_item = arr[idx], arr[idx + 1]
            if curr_item > next_item and sort_incr\
                    or curr_item < next_item and not sort_incr:
                arr[idx], arr[idx + 1] = next_item, curr_item
                is_not_changed = False
        if is_not_changed:
            return arr
    return arr


if __name__ == "__main__":
    # перебираем варианты размерности массива
    for arr_cnt in (100, 1000, 10000):

        # генерация массива случ. целых для послед. сортировки
        arr_for_sort = [randint(-100, 99) for _ in range(arr_cnt)]

        print(f'\nИсходный массив ({arr_cnt} элементов):')
        print(*arr_for_sort if arr_cnt <= 20 else
              (*arr_for_sort[:10], ' ... ', *arr_for_sort[-10:]))

        # сортируем массив нашей функцией и замеряем время
        start_time = default_timer()
        sorted_arr = buble_sort_v1(arr_for_sort[:], sort_incr=False)
        time_sort = default_timer() - start_time

        # сортируем массив модиф. функцией и замеряем время
        start_time = default_timer()
        # здесь отдаем на вход не отсортированный массив
        sorted_arr_mod = buble_sort_v2(arr_for_sort[:], sort_incr=False)
        # здесь пробуем отдать на вход уже отсортированный массив
        # sorted_arr_mod = buble_sort_v2(sorted_arr, sort_incr=False)
        time_sort_mod = default_timer() - start_time

        print(f'Отсортированный по убыванию массив ({arr_cnt} элементов):')
        print(*sorted_arr if arr_cnt <= 20 else
              (*sorted_arr[:10], ' ... ', *sorted_arr[-10:]))

        print(f'Время на сортировку: {time_sort:.4f} сек "пузырьком", '
              f'с модификацией: {time_sort_mod:.4f} сек '
              f'({((time_sort - time_sort_mod) / time_sort_mod):.4f} %)')
