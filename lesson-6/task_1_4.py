"""Задание 1.
Выполните профилирование памяти в скриптах. Проанализируйте результат и
определите программы с наиболее эффективным использованием памяти.

Примечание: Для анализа возьмите любые 3-5 ваших РАЗНЫХ скриптов! (хотя бы 3
разных для получения оценки отл). На каждый скрипт вы должны сделать как
минимум по две реализации.

Можно взять только домашние задания с курса Основ или с текущего курса
Алгоритмов

Результаты профилирования добавьте в виде комментариев к коду. Обязательно
сделайте аналитику (что с памятью в ваших скриптах, в чем ваша оптимизация и
т.д.)

ВНИМАНИЕ: ЗАДАНИЯ, В КОТОРЫХ БУДУТ ГОЛЫЕ ЦИФРЫ ЗАМЕРОВ (БЕЗ АНАЛИТИКИ)
БУДУТ ПРИНИМАТЬСЯ С ОЦЕНКОЙ УДОВЛЕТВОРИТЕЛЬНО

Попытайтесь дополнительно свой декоратор используя ф-цию memory_usage из
memory_profiler С одновременным замером времени (timeit.default_timer())!"""

from os.path import exists
from memory_profiler import memory_usage
from timeit import default_timer
from functools import wraps
import sqlite3


def my_profiler(func):
    """Возвращает кортеж из замеров по декорируемой функции:
    фактическое использование памяти (memory_profiler.memory_usage) и
    времени (timeit.default_timer)"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """используем wraps, чтобы скрыть работу своего декоратора и получать на
        func.__name__ не wrapper, а имя декорируемой функции func"""

        # замеры по потреблению памяти и времени
        time_start = default_timer()
        mem_start = memory_usage()
        result = func(*args, **kwargs)
        mem_usage = memory_usage()[0] - mem_start[0]
        time_usage = default_timer() - time_start

        print(f'При выполнении скрипта {func.__name__} '
              f'было использовано {mem_usage:.6f} Mib ОЗУ, '
              f'время выполнения {time_usage:.6f} сек.')
        return result
    return wrapper


@my_profiler
def simple(i):
    """Наивный поиск i-го простого числа"""
    count, n = 1, 2
    while count <= i:
        t = 1
        is_simple = True
        while t <= n:
            if n % t == 0 and t != 1 and t != n:
                is_simple = False
                break
            t += 1
        if is_simple:
            if count == i:
                break
            count += 1
        n += 1
    return n


@my_profiler
def simple_nums_ertsfn(num_simple, len_arr=0):
    """Вычисляет num_simple-простых чисел алгоритмом Решето Эратосфена"""

    CFC = 11  # по крайней мере до 7000 простого числа - достаточно коэф. 11
    # список заполняем значениями от 0 до num_simple * CFC
    if not len_arr:  # если длина массива не передана явно
        len_arr = (num_simple * CFC)
    simle_arr = []  # сюда будем собирать найденные простые числа
    nums = [num for num in range(len_arr)]
    nums[1] = 0  # 1 - не считают простым числом
    idx = 2  # начинаем с 3-го элемента

    while idx <= len_arr - 1:

        # если значение ячейки было обнулено до этого - там не простое число
        if not nums[idx]:
            idx += 1  # переходим к следующему числу
            continue

        # значение ячейки до этого не было обнулено - там простое число
        not_simple_idx = idx + idx
        simle_arr.append(nums[idx])  # забираем найденное простое число

        # если нашли искомое простое - возвращаем его и дальше не ищем
        if len(simle_arr) == num_simple:
            # тестовая печать
            # print(f'{len(nums)=} {nums[:10]=}...{nums[-10:]=}\n'
            #       f'{len(simle_arr)=} {simle_arr[:10]=}...{simle_arr[-10:]=}')
            return simle_arr[-1]

        # проставляем 0 на всех кратных индексах для составных чисел диапазона
        while not_simple_idx <= len_arr - 1:
            if nums[not_simple_idx] != 0:
                nums[not_simple_idx] = 0
            not_simple_idx += idx
        idx += 1  # переходим к следующему индексу

    # тестовая печать
    # print(f'{len(nums)=} {nums[:10]=} ... {nums[-10:]=}\n'
    #       f'{len(simle_arr)=} {simle_arr[:10]=} ... {simle_arr[-10:]=}')
    # если просеяли весь диапазон, но не нашли искомое по счету простое -
    # вернем последнее найденное
    return simle_arr[-1]


class SimpleNums:
    """Реализует поиск, хранение и выдачу простых чисел"""

    def __init__(self, s_nums_storage_name='SimpleNums.sqlite',
                 s_nums_chunk=100000, db_chunk=1000):

        # путь к файлу-хранилищу
        self.s_nums_storage_name = s_nums_storage_name
        # размер диапазона (чанка) поиска простых чисел
        self.s_nums_chunk = s_nums_chunk
        self.db_chunk = db_chunk
        # результаты запроса простых чисел в виде списка (idx_s_num, s_num)
        self.results = None

        # подключаемся к хранилищу простых чисел
        db_store = sqlite3.connect(self.s_nums_storage_name)
        cursor = db_store.cursor()
        # если нет - создаем таблицу s_nums -
        # idx_s_num (номер прост. числа), s_num - прост. число и индексы для них
        cursor.execute("CREATE TABLE IF NOT EXISTS s_nums ("
                       "id INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,"
                       "idx_s_num INTEGER UNIQUE NOT NULL,"
                       "s_num TEXT UNIQUE NOT NULL)")
        cursor.execute("CREATE INDEX IF NOT EXISTS index_idx_s_num on s_nums "
                       "(idx_s_num)")
        cursor.execute("CREATE INDEX IF NOT EXISTS index_s_num on s_nums "
                       "(s_num)")
        db_store.commit()

        # находим и сохраняем в атрибуты максимальный номер и само простое
        # число из хранилища
        self._get_storage_data()

        # тестовое внесение данных в хранилище
        # test = (1, 2, 3, 5, 7, 9, 11)
        # for idx, num in enumerate(test):
        #     cursor.execute(f'INSERT INTO s_nums (idx_s_num, s_num) VALUES('
        #                    f'{idx + 1}, {str(num)})')
        # db_store.commit()

        db_store.close()

    def _get_storage_data(self, start_idx=None, end_idx=None,
                          start_s_num=None, end_s_num=None):
        """выдает запрошенные данные из хранилища"""

        if start_idx and start_s_num:
            print(f'Нельзя одновременно запрашивать простое число и по его '
                  f'номеру и по значению! Заданы: {start_idx=}, {start_s_num=}')
            exit(1)

        # если задано начало, а конец нет - приравниваем к началу
        if start_idx and end_idx is None:
            end_idx = start_idx
        if start_s_num and end_s_num is None:
            end_s_num = start_s_num

        # подключаемся к хранилищу простых чисел
        db_store = sqlite3.connect(self.s_nums_storage_name)
        cursor = db_store.cursor()

        # находим и сохр. в атрибуты макс. прост. число и его номер из
        # хранилища, если не запрошены ни номера, ни границы простых чисел
        if not any((start_idx, end_idx, start_s_num, end_s_num)):
            cursor.execute("SELECT idx_s_num, s_num FROM s_nums WHERE "
                           "idx_s_num=(SELECT max(idx_s_num) FROM s_nums)")
            self.last_idx_s_num, self.last_s_num = cursor.fetchone()
            db_store.close()
            return self.last_idx_s_num, self.last_s_num

        # если запрошены простые числа по их номеру
        if start_idx and end_idx >= start_idx:
            cursor.execute(f"SELECT idx_s_num, s_num FROM s_nums WHERE "
                           f"idx_s_num >= {start_idx} and "
                           f"idx_s_num <= {end_idx} ORDER BY idx_s_num")
            self.results = cursor.fetchall()
            db_store.close()
            return self.results
        else:
            print(f'Некорректно заданы границы запроса номеров простых чисел в '
                  f'хранилище! {start_idx=}, {end_idx=}')
            exit(1)

        # если запрошены простые числа по их значению
        if start_s_num and end_s_num >= start_s_num:
            cursor.execute(f"SELECT idx_s_num, s_num FROM s_nums WHERE "
                           f"s_num >= {start_s_num} and "
                           f"s_num <= {end_s_num} ORDER BY idx_s_num")
            self.results = cursor.fetchall()
            db_store.close()
            return self.results
        else:
            print(f'Некорректно заданы границы запроса простых чисел в '
                  f'хранилище! {start_s_num=}, {end_s_num=}')
            exit(1)

    def get_idx_s_nums(self, start_idx_s_num=None, end_idx_s_num=None):
        """выдает простое число с номером start_idx_s_num или диапазон
        простых чисел с номерами от start_idx_s_num до end_idx_s_num"""

        assert (start_idx_s_num is None and end_idx_s_num is None) or \
            (start_idx_s_num > 0 and
             (end_idx_s_num is None or end_idx_s_num >= start_idx_s_num)), \
            f"Запрошены некорректные номера простых чисел: " \
            f"{start_idx_s_num=}, {end_idx_s_num=}"

        # если вызвали без параметров или нужно последнее пр. число - просто
        # отдаем последнее из хранилища
        if start_idx_s_num is None and end_idx_s_num is None \
                or start_idx_s_num == self.last_idx_s_num:
            self.results = tuple(self.last_idx_s_num, self.last_s_num)
            return self.results

        # запрошенные номера прост. чисел есть в хранилище - читаем их
        if end_idx_s_num <= self.last_idx_s_num:
            return self._get_storage_data(start_idx=start_idx_s_num,
                                          end_idx=end_idx_s_num)

        # если запрошенного номера простого числа нет в хранилище - вычисляем
        # (сохраняя в хранилище) и отдаем результат
        while end_idx_s_num < self.last_idx_s_num:
            self._calc_s_num(end_idx_s_num=end_idx_s_num)
        return self._get_storage_data(start_idx=start_idx_s_num,
                                      end_s_num=end_idx_s_num)

    def _calc_s_num(self, end_s_num, start_s_num=None):
        """вычисляет простые числа, по запрошенному на заданном отрезке"""

        # если начало отрезка не задано - пляшем от последнего известного
        if start_s_num is None:
            start_s_num = self.last_s_num + 1

        # создаем массив, на котором будем искать простые числа
        nums = {num: num for num in range(start_s_num, end_s_num)}

        print(f'{nums=}')



        while end_idx_s_num < self.last_idx_s_num or \
                end_s_num < self.last_s_num:
            self._calc_s_num(start_s_num=self.last_s_num + 1,
                             end_s_num=self.last_s_num + self.s_nums_chunk)

            # форминуем массив чисел на котором будем искать решетом простые
            nums = {num: num for num in range(start_s_num, end_s_num)}

            # чанками читаем известные простые числа из хранилища и

            while start_s_num < self.last_s_num

            idx = 0  # начинаем с 3-го элемента

            while idx <= len_arr - 1:

                # если значение ячейки было обнулено до этого - там не простое число
                if not nums[idx]:
                    idx += 1  # переходим к следующему числу
                    continue

                # значение ячейки до этого не было обнулено - там простое число
                not_simple_idx = idx + idx
                simle_arr.append(nums[idx])  # забираем найденное простое число

                # если нашли искомое простое - возвращаем его и дальше не ищем
                if len(simle_arr) == num_simple:
                    # тестовая печать
                    # print(f'{len(nums)=} {nums[:10]=}...{nums[-10:]=}\n'
                    #       f'{len(simle_arr)=} {simle_arr[:10]=}...{simle_arr[-10:]=}')
                    return simle_arr[-1]

                # проставляем 0 на всех кратных индексах для составных чисел диапазона
                while not_simple_idx <= len_arr - 1:
                    if nums[not_simple_idx] != 0:
                        nums[not_simple_idx] = 0
                    not_simple_idx += idx
                idx += 1  # переходим к следующему индексу

            # тестовая печать
            # print(f'{len(nums)=} {nums[:10]=} ... {nums[-10:]=}\n'
            #       f'{len(simle_arr)=} {simle_arr[:10]=} ... {simle_arr[-10:]=}')
            # если просеяли весь диапазон, но не нашли искомое по счету простое -
            # вернем последнее найденное
            return simle_arr[-1]


if __name__ == '__main__':

    idx_simple_num = input('Введите порядковый номер искомого простого числа: ')
    try:
        idx_simple_num = int(idx_simple_num)
        if idx_simple_num < 1:
            raise ValueError
    except ValueError:
        print(f'Необходимо ввести целое положительное число, введено '
              f'{idx_simple_num}!')
        exit(1)

    print(f'Наивный алгоритм поиска простого числа'
          f' №{idx_simple_num}: {simple(idx_simple_num)}\n')

    print(f'Алгоритм "Решето Эратосфена" поиска простого числа '
          f'№{idx_simple_num}: {simple_nums_ertsfn(idx_simple_num)}\n')

    # оптимизированный алгоритм на базе "Решето Эратосфена"
    ertsfn = SimpleNums()
    temp = ertsfn.get_idx_s_nums(start_idx_s_num=3, end_idx_s_num=6)
    print(temp)

"""
"""
