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

from memory_profiler import profile, memory_usage
from timeit import default_timer
from functools import wraps


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


# оба декоратора сразу - не работают - запускаем по-очереди
@my_profiler
# @profile
def func_1_1(log_file_name='', pars_log_file_name=''):
    """Реализация скрипта парсинга лога nginx_logs без оптимизации по памяти"""
    import re

    PATH_LOG_FILE = "nginx_logs.txt"
    PATH_PARS_LOG = "pars_nginx_logs(func_1_1).txt"
    RE_PATTERN = r"(?P<remote_addr>^.+)(?: - - )(?:\[" \
                 r"(?P<req_datetime>.+)\]+)(?: \"" \
                 r"(?P<req_type>[A-Z]+) )" \
                 r"(?P<req_resource>[/\w\d]+)( [\w\d/.]+\" )" \
                 r"(?P<resp_code>\d+) " \
                 r"(?P<resp_size>\d+)"

    def log_parser(log_lines: list, cmp_pattern):
        """Парсит переданный массив строк лога (вида nginx_logs) в соответствии
        с компилированным (re) шаблоном cmp_pattern, отдает список tupple вида:
        (remote_addr, request_datetime, request_type, requested_resource,
        response_code, response_size)"""
        res_pars = []
        for line in log_lines:
            result = cmp_pattern.search(line)
            res_pars.append(tuple(result.groupdict().values()))
        return res_pars

    re_pattern = re.compile(RE_PATTERN)

    # если имена/пути к файлам лога и результатам парсинга не заданы - по-умолч.
    path_log_file = log_file_name if log_file_name else PATH_LOG_FILE
    path_pars_log_file = pars_log_file_name if pars_log_file_name else \
        PATH_PARS_LOG

    # считаем, что лог сильно меньше ОЗУ - читаем лог целиком
    try:
        with open(path_log_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except IOError as err:
        print(f'Сбой операции чтения файла {path_log_file}: {err.strerror}')

    pars_data = log_parser(content, re_pattern)

    try:
        with open(path_pars_log_file, 'w', encoding='utf-8') as f:
            for pars_line in pars_data:
                f.write(f"{pars_line}\n")
    except IOError as err:
        print(f'Сбой операции записи файла {path_pars_log_file}:'
              f' {err.strerror}')

    print(f'\nФункцией func_1_1 распарсено {len(pars_data):,d} строк файла'
          f' {path_log_file}.\n'
          f'Результат парсинга сохранен в файл {path_pars_log_file}')


# оба декоратора сразу - не работают - запускаем по-очереди
@my_profiler
# @profile
def func_1_2(log_file_name='', pars_log_file_name=''):
    """Реализация скрипта парсинга лога nginx_logs c оптимизацией по памяти"""
    import re

    PATH_LOG_FILE = "nginx_logs.txt"
    PATH_PARS_LOG = "pars_nginx_logs(func_1_2).txt"
    RE_PATTERN = r"(?P<remote_addr>^.+)(?: - - )(?:\[" \
                 r"(?P<req_datetime>.+)\]+)(?: \"" \
                 r"(?P<req_type>[A-Z]+) )" \
                 r"(?P<req_resource>[/\w\d]+)( [\w\d/.]+\" )" \
                 r"(?P<resp_code>\d+) " \
                 r"(?P<resp_size>\d+)"

    re_pattern = re.compile(RE_PATTERN)

    # если имена/пути к файлам лога и результатам парсинга не заданы - по-умолч.
    path_log_file = log_file_name if log_file_name else PATH_LOG_FILE
    path_pars_log_file = pars_log_file_name if pars_log_file_name else \
        PATH_PARS_LOG

    # т.к. лог может быть очень большим - будем анализировать построчно
    try:
        # читаем строку, анализируем и сразу пишем результат в файл
        with open(path_log_file, 'r', encoding='utf-8') as lf,\
                open(path_pars_log_file, 'w', encoding='utf-8') as plf:
            # проходим по всем строкам лога
            for idx_line, log_line in enumerate(lf):
                # ищем регуляркой данные в текущей строке лога
                res_search = re_pattern.search(log_line)
                # собираем найденные данные в кортеж
                res_parsing = tuple(res_search.groupdict().values())
                plf.write(f"{res_parsing}\n")
                cnt_lines = idx_line
    except IOError as err:
        print(f'Сбой операций с файлами: {err}')

    print(f'\nФункцией func_1_2 распарсено {(cnt_lines + 1):,d} строк файла'
          f' {path_log_file}.\n'
          f'Результат парсинга сохранен в файл {path_pars_log_file}')


if __name__ == '__main__':
    func_1_1()  # замеры по функции без оптимизации по памяти
    func_1_2()  # замеры по функции с оптимизацией по памяти


"""
Анализ через декоратор @profile:
--------------------------------
func_1_1()
Основное потребление памяти в скрипте происходит при считывании сразу всего 
содержимого лог-файла и сохранения результата парсинга каждой строки в список 
кортежей с данными. При увеличении размера анализируемого лога - потребление 
памяти будет расти пропорционально.

func_1_2()
Потребление памяти скриптом оптимизировано за счет построчной работы - 
происходит считывание строки, ее парсинг и сразу сохранение результата в 
файл, за счет чего потребление ОЗУ не будет зависеть от размера 
обрабатываемого лог-файла. 


Анализ через декоратор @my_profiler:
------------------------------------
В декораторе производится замеры по реальному потреблению памяти 
(memory_profiler.memory_usage), а также время работы скрипта.

По потреблению памяти видим (при парсинге файла 51к строк) существенную 
разницу (примерно на 2 порядка в данном конкретном случае) при работе 
построчно, а не со всем файлом сразу, при этом время выполнения обоих скриптов 
практически одинаково.
"""
