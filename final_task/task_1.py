''' Задание 1.
Определение количества различных подстрок с использованием хэш-функции.
Пусть дана строка S длиной N, состоящая только из маленьких латинских букв.
Требуется найти количество различных подстрок в этой строке.
Примечание:в сумму не включаем пустую строку и строку целиком.'''

import hashlib


def get_cnt_diff_substr_ver_set(str_in):
    '''Возвращает кол-во уникальных подстрок в переданной строке,
    без учета пустых строк и самой строки в целом. Решение через множества.'''

    if len(str_in) < 2:
        return 0
    set_of_substr = set()
    for len_substr in range(1, len(str_in)):
        start_idx = 0  # начальная позиция "окна" для прохождения по строке
        # проходим окном выбранного размера по всей строке до конца
        while (start_idx + len_substr) <= len(str_in):
            # выделяем текущую подстроку для анализа
            curr_substr = str_in[start_idx:start_idx + len_substr]

            # отладочная информация
            # is_uniq_substr = False if curr_substr in set_of_substr else True
            # print(f'{len_substr=}, {start_idx=}, {curr_substr=}, '
            #       f'{is_uniq_substr=}, {set_of_substr=}')

            # если подстрока уникальная - добавится в множество
            set_of_substr.add(curr_substr)
            start_idx += 1  # сдвигаем начало "окна" подстроки
    # итоговое множество с уникальными подстроками
    # print(f'{set_of_substr=}')
    return len(set_of_substr)  # возвращаем кол-во уникальных подстрок


def get_cnt_diff_substr_ver_hash(str_in):
    '''Возвращает кол-во уникальных подстрок в переданной строке,
    без учета пустых строк и самой строки в целом. Решение через хеши'''

    if len(str_in) < 2:
        return 0
    lst_of_hashes_substr = []
    for len_substr in range(1, len(str_in)):
        start_idx = 0  # начальная позиция "окна" для прохождения по строке
        # проходим окном выбранного размера по всей строке до конца
        while (start_idx + len_substr) <= len(str_in):
            # выделяем текущую подстроку для анализа
            curr_substr = str_in[start_idx:start_idx + len_substr]
            hash_curr_substr = hashlib.sha1(curr_substr.encode('utf-8')).hexdigest()
            is_uniq_substr = False if hash_curr_substr in lst_of_hashes_substr \
                else True

            # отладочная информация
            # print(f'{len_substr=}, {start_idx=}, {hash_curr_substr=}, {curr_substr=}, '
            #       f'{is_uniq_substr=}, {lst_of_hashes_substr=}')

            # если подстрока уникальная - добавляем в список хешей
            if is_uniq_substr:
                lst_of_hashes_substr.append(hash_curr_substr)
            start_idx += 1  # сдвигаем начало "окна" подстроки

    # итоговое множество с уникальными подстроками
    # print(f'{lst_of_hashes_substr=}')

    return len(lst_of_hashes_substr)  # возвращаем кол-во уникальных подстрок


if __name__ == '__main__':
    # str_in = input('Введите строку для поиска количества уникальных подстрок: ')
    str_in = 'abracadabra'
    print(f'Количество уникальных подстрок в строке {str_in}:',
          f'- через множества: {get_cnt_diff_substr_ver_set(str_in)}',
          f'- через хеши: {get_cnt_diff_substr_ver_hash(str_in)}', sep='\n')
