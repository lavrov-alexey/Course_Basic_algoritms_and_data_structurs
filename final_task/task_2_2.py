"""Задание 2. Закодируйте любую строку из трех слов по алгоритму Хаффмана
Вариант 2. Хаффман через ООП
Решение полностью идентично решению задания 8.1.2"""

import heapq  # станд. модуль работы с минимальной кучей
from collections import Counter  # словарь счетчиков частот объектов в коллекции
from collections import namedtuple  # именованные кортежи


# вспомогательные классы для хранения информации о структуре дерева
class Node(namedtuple('Node', ['left', 'right'])):
    """Класс для ветвей дерева (внутренних узлов) с потомками"""
    def walk(self, code, acc):
        """Метод обхода дерева"""
        # идем в левого потомка, добавив к префиксу '0'
        self.left.walk(code, acc + '0')
        # идем в правого потомка, добавив к префиксу '1'
        self.right.walk(code, acc + '1')

class Leaf(namedtuple('Leaf', ['element'])):
    """Класс для листьев дерева, нет потомков, но есть значение элемента"""
    def walk(self, code, acc):
        # потомков нет, поэтому для значения записываем код для данного элемента
        code[self.element] = acc or '0'
        # если последовательность для кодирования длиной 1, то acc='' (False)
        # в этом случае - установим значение acc='0' (True)

class HaffmanCode():
    """Класс, реализующий кодирование/декодирование последовательности
    по алгоритму Хаффмана
    dec_sequence: входная последовательность для кодирования
    enc_sequence: входная последовательность для декодирования
    code_dict: словарь элементов последовательности и их кодов по Хаффману
    result: кодированная/декодированная последовательность"""

    def __init__(self, enc_sequence='', dec_sequence='',
                 code_dict={}):
        self.enc_sequence = enc_sequence
        self.dec_sequence = dec_sequence
        self.code_dict = code_dict

    def encode(self, dec_sequence):
        """Метод кодирования последовательности по Хаффману"""
        self.dec_sequence = dec_sequence
        queue_items = []  # очередь элементов
        # строим очередь с добавлением счетчика элемента
        for item, freq in Counter(self.dec_sequence).items():
            # в очереди будет кортежи из частоты, индекса и собственно элемента
            queue_items.append((freq, len(queue_items), Leaf(item)))
        # строим очередь с приоритетами - загоняя очередь в "мин. кучу"
        # print(f'{queue_items=}')  # неотсортированная по частотам очередь
        heapq.heapify(queue_items)
        # print(f'{queue_items=}')  # отсортированная по возраст. частот очередь
        cnt_queue = len(queue_items)  # инициализируем счетчик длиной очереди

        # пока в очереди есть хотя бы 2 элемента
        while len(queue_items) > 1:
            # вытаскиваем 2 элемента с минимальными частотами - левый и пр. узлы
            freq_left, _cnt_left, left = heapq.heappop(queue_items)
            freq_right, _cnt_right, right = heapq.heappop(queue_items)

            # помещаем в очередь новый элемент, у которого частота равна сумме
            # частот вытащенных элементов, а сам элемент - это новый узел
            # дерева, у которого потомки left и right
            new_item = (freq_left + freq_right, cnt_queue, Node(left, right))
            heapq.heappush(queue_items, new_item)
            # инкр. счетчик очереди при добавлении нов. эл-та дерева
            cnt_queue += 1

        # наполняем словарь кодов элементов последовательности для кодирования
        # если вход. послед-сть пустая => очередь - пустая и обходить нечего
        if queue_items:
            # в очереди 1 эл-т (корень дерева), приоритет его - не важен
            [(_freq, _cnt, root)] = queue_items
            # обходим дерево от корня и заполняем словарь кодов элементов
            root.walk(self.code_dict, '')
        # возвращаем словарь элементов и соотв. им кодов по Хаффману
        return self.code_dict

    def decode(self, enc_sequence, code_dict):
        """Метод декодирования последовательности шифрованной по Хаффману
        последовательности enc_sequence в соответствии со словарем кодов
        элементов послед. code_dict"""
        self.enc_sequence = enc_sequence
        self.code_dict = code_dict
        dec_sequence = []  # сюда будем набирать раскодированные элементы
        enc_el = ''  # значение закодированного элемента
        # обходим все элементы закодированной последовательности
        for item in self.enc_sequence:
            enc_el += item  # добавляем текущий элемент к закодированному
            # пробуем найти закодированный символ в словаре кодов
            for dec_el in self.code_dict:
                # если закодированный элемент найден
                if self.code_dict.get(dec_el) == enc_el:
                    # добавляем значение раскод. эл-та к раскодир. послед-сти
                    dec_sequence.append(dec_el)
                    enc_el = ''  # сбрасываем знач. закодированного эл-та
                    break  # переходим к поиску значения след. элемента
        # соединяем все декодированные элементы в строку и возвращаем ее
        self.dec_sequence = ''.join(dec_sequence)
        return self.dec_sequence


def main():
    """Клиентский код для тестов"""
    in_str = input("Введите строку для кодирования по Хаффману: ")
    code_dict = HaffmanCode().encode(dec_sequence=in_str)
    # отобразим закодированную версию, отобразив каждый символ со своим кодом
    encoded = ''.join(code_dict[el] for el in in_str)
    print(f'Закодированная по Хаффману последовательность: {encoded}')
    # раскодируем обратно
    decoded = HaffmanCode().decode(enc_sequence=encoded, code_dict=code_dict)
    print(f'Декодированная обратно последовательность: {decoded}')
    print(f'Кол-во элементов в словаре кодов: {len(code_dict)}')
    print(f'Длина последовательности - исходная: '
          f'{len(in_str.encode("utf-8")) * 8} бит, '
          f'закодированная: {len(encoded)} бит')
    print('Элементы последовательности и их коды:')
    for el, code in code_dict.items():
        print(f'"{el}": {code}')


if __name__ == '__main__':
    main()
