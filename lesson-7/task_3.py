import random
from statistics import median
from timeit import default_timer

"""3. Массив размером 2m + 1, где m – натуральное число, заполнен случайным
образом. Найдите в массиве медиану. Медианой называется элемент ряда, делящий
его на две равные по длине части: в одной находятся элементы, которые не меньше
медианы, в другой – не больше медианы.
Задачу можно решить без сортировки исходного массива.
Но если это слишком сложно, то используйте метод сортировки, который
не рассматривался на уроках: Шелла, Гномья, Кучей...
Важно: стройте массив именно по формуле 2m+1
Потому что параметр m вам пригодится при поиске медианы,
когда массив будет отсортирован.
Этот параметр m вам нужно запрашивать у пользователя.
[5, 3, 4, 3, 3, 3, 3]
[3, 3, 3, 3, 3, 4, 5]
my_lst
new_lts
arr[m]
from statistics import median
[3, 4, 3, 3, 5, 3, 3]
left = []
right = []
left == right and
for i in
    for
    left == right
    left.clear()
    right.clear()
"""

"""ВЫВОДЫ 
Наилучшее время показали варианты использования встроенных в Python сортировки 
массива и использования модуля статистики.
Наихудшее время - "Гномья" сортировка."""


def shell_sort(arr, step='auto'):
    """Сортирует массив алгоритмом Шелла. Сложность O(N**2), выбор шага важен -
    в некоторых вариантах сложность алгоритма улучшается до О(N**3/2)"""
    if step == 'auto':  # если шаг не передали "снаружи" - выбираем сами
        step = len(arr) // 2  # шаг по Д.Шеллу: D(i)=N/2
    # сортируем, пока шаг больше или равен 1
    while step:
        # начинаем с элемента с индексом шага и идем до конца массива
        for curr_idx in range(step, len(arr)):
            step_idx = curr_idx
            while step_idx >= step and arr[step_idx - step] > arr[step_idx]:
                # пока можем шагать влево и эл-т левее на шаг больше, чем справа
                # меняем их местами
                arr[step_idx - step], arr[step_idx] = \
                    arr[step_idx], arr[step_idx - step]
                # сдвигаемся на шаг влево
                step_idx = step_idx - step
        step //= 2  # уменьшение шага по Д.Шеллу D(i+1) = D(i)/2
    return arr


def heap_sort(arr):
    """Сортировка кучей (пирамидальная сортировка) массива заданного размера.
    Сложность алгоритма O(N*LogN)"""

    def heapify(arr, heap_size, idx_root):
        """Преобразует массив в двоичную кучу поддерева с корневым
        узлом arr[idx_root], heap_size - размер кучи"""
        idx_largest = idx_root  # инициал. наибольшее знач. как корень дерева
        idx_left = 2 * idx_root + 1  # индекс левого элемента корня
        idx_right = 2 * idx_root + 2  # и правого

        # Проверяем существует ли левый дочерний элемент больший, чем корень
        if idx_left < heap_size and arr[idx_root] < arr[idx_left]:
            idx_largest = idx_left

        # Проверяем существует ли правый дочерний элемент больший, чем корень
        if idx_right < heap_size and arr[idx_largest] < arr[idx_right]:
            idx_largest = idx_right

        # Заменяем корень, если нужно на больший элемент
        if idx_largest != idx_root:
            arr[idx_root], arr[idx_largest] = arr[idx_largest], arr[idx_root]
            # Применяем heapify к корню.
            heapify(arr, heap_size, idx_largest)

    # Основной алгоритм сортировки
    heap_size = len(arr)

    # построение max-heap
    for idx in range(heap_size, -1, -1):
        heapify(arr, heap_size, idx)

    # один за другим извлекаем элементы
    for idx in range(heap_size-1, 0, -1):
        arr[idx], arr[0] = arr[0], arr[idx]  # обмен элементов
        heapify(arr, idx, 0)

    return arr  # возвращаем отсортированный массив


def dwarf_sort(arr):
    """Сортирует массив arr 'гномьей' сортировкой. Сложность О(N2)"""
    mem_idx = 1   # индекс массива для возврата после отшагивания назад
    curr_idx = 0  # текущий индекс массива
    last_idx = len(arr) - 1  # индекс последнего элемента массива
    # пока не дошли до посл. элемента
    while curr_idx < last_idx:
        if arr[curr_idx] <= arr[curr_idx + 1]:
            # если текущ. эл-т массива не больше следующего - сдвигаемся вперед
            curr_idx, mem_idx = mem_idx, mem_idx + 1
        else:
            # если нет - меняем элементы местами
            arr[curr_idx], arr[curr_idx + 1] = arr[curr_idx + 1], arr[curr_idx]
            # если дошли до начала, то возвращаемся к сорт. с сохр. позиции
            curr_idx -= 1
            if curr_idx < 0:
                curr_idx, mem_idx = mem_idx, mem_idx + 1
    return arr


def quick_select_median(arr, find_idx):
    """
    Ищет медиану неупорядоченного массива с нечетн. кол-вом эл-тов по алгоритму
    quickselect Тони Хоара. Средняя сложность O(N).
    :param arr: массив для поиска
    :find_idx: индекс медианы
    :return: медиана массива arr
    """

    # крайний случай: если у нас массив из 1 эл-та
    if len(arr) == 1:
        assert find_idx == 0  # искать можно только 0-ой эл-т
        return arr[0]

    # выбираем опорный эл-т с помощью спец. функции выбора
    pivot = random.choice(arr)

    # делим все элементы массива на большие, меньшие и равные опорному
    lows = [el for el in arr if el < pivot]
    highs = [el for el in arr if el > pivot]
    pivots = [el for el in arr if el == pivot]

    if find_idx < len(lows):
        # медиана - в массиве эл-тов, меньше опорного - ищем дальше там
        return quick_select_median(lows, find_idx)
    elif find_idx < len(lows) + len(pivots):
        # повезло - медиана угадана!
        return pivots[0]
    else:
        # медиана - в массиве эл-тов, больше опорного - ищем дальше там
        return quick_select_median(highs, find_idx - len(lows) - len(pivots))


if __name__ == '__main__':
    START_VAL, END_VAL = 0, 1000000

    half_len_arr = int(input('Введите половину длинны массива для сортировки'
                             ' (2*m + 1), m = '))
    len_arr = 2 * half_len_arr + 1
    arr_for_sort = [random.randint(START_VAL, END_VAL) for _ in range(len_arr)]
    print(f'\nИсходный массив (случ. числа от {START_VAL} до {END_VAL}): ',
          *arr_for_sort if len_arr < 30 else
          (*arr_for_sort[:10], ' ... ', *arr_for_sort[-10:]))

    start_time = default_timer()
    sorted_arr = shell_sort(arr_for_sort[:])
    print('\nСорт. Шелла:  ', *sorted_arr if len_arr < 30 else
          (*sorted_arr[:10], ' ... ', *sorted_arr[-10:]))
    print(f'Медиана массива: {sorted_arr[half_len_arr]}, '
          f'затраты времени: {(default_timer() - start_time):.6f} сек.')

    start_time = default_timer()
    sorted_arr = heap_sort(arr_for_sort[:])
    print('\nСорт. кучей:  ', *sorted_arr if len_arr < 30 else
          (*sorted_arr[:10], ' ... ', *sorted_arr[-10:]))
    print(f'Медиана массива: {sorted_arr[half_len_arr]}, '
          f'затраты времени: {(default_timer() - start_time):.6f} сек.')

    start_time = default_timer()
    sorted_arr = dwarf_sort(arr_for_sort[:])
    print('\nГномья сорт.: ', *sorted_arr if len_arr < 30 else
          (*sorted_arr[:10], ' ... ', *sorted_arr[-10:]))
    print(f'Медиана массива: {sorted_arr[half_len_arr]}, '
          f'затраты времени: {(default_timer() - start_time):.6f} сек.')

    start_time = default_timer()
    sorted_arr = sorted(arr_for_sort[:])
    print('\nВстроенная сортировка:  ', *sorted_arr if len_arr < 30 else
          (*sorted_arr[:10], ' ... ', *sorted_arr[-10:]))
    print(f'Медиана массива: {sorted_arr[half_len_arr]}, '
          f'затраты времени: {(default_timer() - start_time):.6f} сек.')

    start_time = default_timer()
    print(f'\nМедиана массива (statistics.median): {median(arr_for_sort)}, '
          f'затраты времени: {(default_timer() - start_time):.6f} сек.')

    start_time = default_timer()
    print(f'\nМедиана массива без сортировки (quickselect Тони Хоара): '
          f'{quick_select_median(arr_for_sort[:], half_len_arr)}, '
          f'затраты времени: {(default_timer() - start_time):.6f} сек.')
