import os
import json
import sqlite3
from hashlib import sha256
from uuid import uuid4
from memory_profiler import profile, memory_usage
from pympler import asizeof
from timeit import default_timer
from functools import wraps

"""Задание 2.
Ваша программа должна запрашивать пароль. Для этого пароля вам нужно получить
хеш, используя функцию sha256. Для генерации хеша обязательно нужно использовать
криптографическую соль. Обязательно выведите созданный хеш.
Далее программа должна запросить пароль повторно. Вам нужно проверить, совпадает
ли пароль с исходным. Для проверки необходимо сравнить хеши паролей.
Самый просто вариант хранения хешей - просто в оперативной памяти (в переменных)

ПРИМЕР:
Введите пароль: 123
В базе данных хранится строка:
555a3581d37993843efd4eba1921f1dcaeeafeb855965535d77c55782349444b
Введите пароль еще раз для проверки: 123
Вы ввели правильный пароль

Обязательно усложните задачу!
Добавьте сохранение хеша в файле и получение его из файла. А если вы знаете как
через Python работать с БД, привяжите к заданию БД и сохраняйте хеши там."""

"""Оптимизация по памяти в классе HashStorageOpt заключается в использовании 
слотов в классе (что уже сразу в 2, а дальше и более раз дает выигрыш по 
памяти), а также в том, что известные хеши и 'соли' к ним не считываются 
целиком из файла-хранилища, а получаются по мере необходимости (ленивые 
вычисления), что позволяет убрать линейную зависимость потребления памяти в 
зависимости от размера хранилища.
Подключение к БД производится при создании экземпляра класса, а отключение - 
при уничтожении экземпляра. "Курсор" создается и закрывается при каждом 
обращении к БД в методах класса."""


class HashStorage:
    """хранилище хешей паролей (с 'солью') в json-файле"""

    def __init__(self, storage=None, storage_file='hashes.json'):
        self._name = 'HashStorage'
        # хранилище хешей - dict(хеш_пароля: соль), путь к хранилищу
        self.storage = storage if storage else dict()
        self.storage_file = storage_file
        # текущие - пароль, хеш пароля, соль, хеш "соленого" пароля
        self._pwd = ''
        self.hash_pwd = ''
        self._salt = ''
        self.salted_hash = ''

    def is_hash_in_storage(self):
        """Проверка наличия хеша введенного пароля в хранилище"""
        if self.hash_pwd in self.storage:
            # достаем для имеющегося в хранилище хеша пароля соль
            self._salt = self.storage[self.hash_pwd]
            return True
        return False  # если хеша пароля в хранилище нет

    def write_hash(self, salt='auto'):
        """Расчет хеша (с 'солью'), сохранение в хранилище"""
        # если соль не дана в параметрах, то генерим ее
        self._salt = uuid4().hex if salt == 'auto' else salt
        # сохраняем "соль" для пароля в хранилище
        self.storage[self.hash_pwd] = self._salt
        # сохраняем хеш для "соленого" пароля
        self.salted_hash = sha256(self._salt.encode() +
                                  self._pwd.encode()).hexdigest()

    def get_pwd_hash(self):
        """Вычисление хеша пароля (без 'соли')"""
        self.hash_pwd = sha256(self._pwd.encode()).hexdigest()

    def get_salted_hash(self):
        """Вычисление хеша 'соленого' пароля"""
        self.salted_hash = sha256(self._salt.encode() +
                                  self._pwd.encode()).hexdigest()
        self._pwd = ''  # зачищаем открытый пароль

    def read_storage(self):
        """Чтение хранилища хешей из файла"""
        if not os.path.exists(self.storage_file):
            self.storage = dict()
            return
        with open(self.storage_file, 'r', encoding='utf-8') as storage:
            self.storage = json.load(storage)

    def write_storage(self):
        """Запись хранилища хешей в файл"""
        with open(self.storage_file, 'w', encoding='utf-8') as storage:
            json.dump(self.storage, storage)

    def __str__(self):
        """представление для печати"""
        return f'Class: {self._name}'


class HashStorageOpt:
    """опт. по памяти хранилище хешей паролей (с 'солью') в БД SQLite"""

    # для экономии памяти - используем в классе слоты
    __slots__ = ['_name', 'hashes_db_name', 'db_store_conn',
                 '_pwd', 'hash_pwd', '_salt', 'salted_hash']

    def __init__(self, hashes_db_name='hashes.sqlite'):
        """Инициализирует экземпляр, если нет - создает хранилище БД SQLite"""
        self._name = 'HashStorageOpt'
        # текущие - пароль, хеш пароля, соль, хеш "соленого" пароля
        self._pwd = ''
        self.hash_pwd = ''
        self._salt = ''
        self.salted_hash = ''
        # имя (путь) к файлу БД SQLite с хешами
        self.hashes_db_name = hashes_db_name
        # если нет - создаем таблицу хешей с полями: hash_pwd - хеш пароля,
        # _salt - соль для данного пароля/хеша, а также - индексы для них
        query_create_table = '''CREATE TABLE IF NOT EXISTS hashes (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                  hash_pwd TEXT UNIQUE NOT NULL,
                                  salt TEXT UNIQUE NOT NULL);
                                CREATE INDEX IF NOT EXISTS index_hash_pwd 
                                  on hashes (hash_pwd);
                                CREATE INDEX IF NOT EXISTS index_salt 
                                  on hashes (salt);'''
        # создаем подключение к БД и если нет - создаем таблицу
        try:
            self.db_store_conn = sqlite3.connect(self.hashes_db_name)
            cursor = self.db_store_conn.cursor()
            cursor.executescript(query_create_table)
            self.db_store_conn.commit()
            cursor.close()
        except sqlite3.DatabaseError as error:
            print(f'Ошибка при работе с БД ({self.hashes_db_name}): {error}')

    def __del__(self):
        """Закрываем подключение к БД при уничтожении объекта класса"""
        self.db_store_conn.close()

    def is_hash_in_storage(self):
        """Проверяет наличие хеша введенного пароля в хранилище, если есть -
        сохраненяет в атрибуты "соль" пароля"""
        try:
            cursor = self.db_store_conn.cursor()
            # ищем в БД хеш пароля из атрибута
            query_select_one = """SELECT salt FROM hashes WHERE hash_pwd = ?"""
            cursor.execute(query_select_one, (self.hash_pwd,))
            result_query = cursor.fetchone()
            # если нашли - запоминаем "соль", нет - "пустая соль"
            self._salt = result_query[0] if result_query else ''
            cursor.close()
        except sqlite3.DatabaseError as error:
            print(f'Ошибка при работе с БД ({self.hashes_db_name}): {error}')
            self._salt = ''

        #  если нашли ("соль" не "пустая") => True, иначе => False
        return True if self._salt else False

    def write_to_storage(self, salt='auto'):
        """Расчет хеша (с "солью"), сохранение в хранилище"""
        # если "соль" не дана в параметрах - генерим ее
        self._salt = uuid4().hex if salt == 'auto' else salt

        # сохраняем из атрибутов хеш пароля и "соль" для пароля в хранилище
        try:
            cursor = self.db_store_conn.cursor()
            query_insert = """INSERT INTO hashes (hash_pwd, salt) 
                                  VALUES (?, ?)"""
            cursor.execute(query_insert, (self.hash_pwd, self._salt))
            self.db_store_conn.commit()
            cursor.close()
        except sqlite3.DatabaseError as error:
            print(f'Ошибка при работе с БД ({self.hashes_db_name}): {error}')

        # вычисляем и сохраняем хеш "соленого" пароля в атрибуты
        self.salted_hash = sha256(self._salt.encode() +
                                  self._pwd.encode()).hexdigest()
        # сразу после расчета хеша затираем открытый пароль и работаем с хешем
        self._pwd = ''

    def get_pwd_hash(self):
        """Вычисление хеша пароля (без "соли")"""
        self.hash_pwd = sha256(self._pwd.encode()).hexdigest()

    def get_salted_hash(self):
        """Вычисление хеша "соленого" пароля"""
        self.salted_hash = sha256(self._salt.encode() +
                                  self._pwd.encode()).hexdigest()
        self._pwd = ''  # зачищаем открытый пароль

    def show_storage(self, limit_records=50):
        """Возвращает limit_records записей из БД хранилища хешей"""
        try:
            cursor = self.db_store_conn.cursor()
            query_select_chunk = 'SELECT * FROM hashes LIMIT ?'
            cursor.execute(query_select_chunk, (limit_records,))
            db_data = cursor.fetchall()  # если не нашлось - будет None
        except sqlite3.DatabaseError as error:
            print(f'Ошибка при работе с БД ({self.hashes_db_name}): {error}')
            db_data = None
        finally:
            self.db_store_conn.close()
        # возвращаем выборку из БД или пустую строку, если ничего не нашлось
        return db_data if db_data else ''

    def __str__(self):
        """представление для печати"""
        return f'Class: {self._name}'


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
        mem_start = memory_usage(max_usage=True, interval=0.001,
                                 include_children=True)
        # немного другой вариант замера
        # mem_usage, result = memory_usage(proc=(func, args, kwargs),
        #                                  retval=True, max_usage=True,
        #                                  interval=0.01,
        #                                  include_children=True)
        result = func(*args, **kwargs)
        mem_end = memory_usage(max_usage=True, interval=0.001,
                               include_children=True)
        mem_usage = mem_end - mem_start
        time_usage = default_timer() - time_start

        storage = args[1]
        print(f'При выполнении скрипта {func.__name__} с хранилищем: '
              f'"{str(storage)}", size={asizeof.asizeof(storage)} байт '
              f'было использовано {(mem_usage * 1000):.4f} kib ОЗУ, '
              f'время выполнения {time_usage:.4f} сек.')
        return result
    return wrapper


# оба декоратора сразу - не работают - запускаем по-очереди
@my_profiler
# @profile
def use_hash_storage(pwd, storage):
    """проверяет наличие пароля _pwd в объекте-хранилище storage класса
    HashStorage или HashStorageOpt"""

    assert isinstance(storage, (HashStorage, HashStorageOpt)), \
        f'Передан объект {storage=}, типа: {type(storage)}!'

    storage._pwd = pwd
    res = None

    # обычное хранилище
    if isinstance(storage, HashStorage):
        storage.read_storage()  # считываем из файла хранилище хешей в атрибуты
        storage.get_pwd_hash()  # получаем хеш пароля (без соли)
        if storage.is_hash_in_storage():  # если хеш пароля есть в хранилище
            storage.get_salted_hash()  # получаем хеш "соленого" пароля
            res = f'\nВведенный пароль есть в хранилище' \
                  f' {storage.storage_file}!' \
                  f'\nХеш пароля (без "соли"): {storage.hash_pwd=}' \
                  f'\n"Cоль": {storage._salt=}' \
                  f'\nХеш "соленого" пароля: {storage.salted_hash=}\n'
        else:  # хеша введенного пароля нет в хранилище
            storage.write_hash()  # генерим "соль", хеш и сохраняем в хранилище
            storage.write_storage()  # сохраняем хранилище в файл
            res = f'\nВведенного пароля в хранилище {storage.storage_file} ' \
                  f'нет - сохраняем его там!' \
                  f'\nХеш пароля (без "соли"): {storage.hash_pwd=}' \
                  f'\n"Cоль": {storage._salt=}' \
                  f'\nХеш "соленого" пароля: {storage.salted_hash=}\n'

    # оптимизированное хранилище
    if isinstance(storage, HashStorageOpt):
        storage.get_pwd_hash()
        if storage.is_hash_in_storage():
            # хеш пароля есть в хранилище
            storage.get_salted_hash()
            res = f'\nВведенный пароль есть в оптимизированном хранилище ' \
                  f'{storage.hashes_db_name}!\n' \
                  f'Хеш пароля (без "соли"): {storage.hash_pwd=}\n' \
                  f'"Cоль": {storage._salt=}\n' \
                  f'Хеш "соленого" пароля: {storage.salted_hash=}\n'
        else:
            # хеша пароля нет в хранилище - генерим "соль" и пишем его
            storage.write_to_storage()
            res = f'\nВведенного пароля в хранилище {storage.hashes_db_name} ' \
                  f'нет - сохраняем его там!\n' \
                  f'Хеш пароля (без "соли"): {storage.hash_pwd=}\n' \
                  f'"Cоль": {storage._salt=}\n' \
                  f'Хеш "соленого" пароля: {storage.salted_hash=}\n'

    return res


if __name__ == '__main__':
    hashes = HashStorage()  # создаем экземпляр хранилища с пар-ми по-умолчанию
    hashes_opt = HashStorageOpt()  # создаем экз-р оптимизированного хранилища

    # бесконечный основной цикл скрипта с вводом пароля (пока не введен '0')
    while True:
        # получаем пароль от пользователя и пишем в атрибуты обоих хранилищ
        pswd = input('\nВведите пароль (0 - для выхода из скрипта): ')
        if pswd == '0':
            print('\nВЫХОД ИЗ ПРОГРАММЫ!')
            print(f'В хранилище хешей {hashes.storage_file}: '
                  f'{len(hashes.storage)} записей')
            print(f'В оптимизированном хранилище хешей '
                  f'{hashes_opt.hashes_db_name}: '
                  f'{len(hashes_opt.show_storage())} записей')
            exit(0)

        # используем оба хранилища с введенным паролем и выводим результат
        print(use_hash_storage(pswd, hashes),
              use_hash_storage(pswd, hashes_opt))

        continue  # запрашиваем следующий пароль в осн. цикле скрипта
