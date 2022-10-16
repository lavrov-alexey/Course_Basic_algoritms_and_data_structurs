from random import randint

""" Задание 8.2. Доработайте пример структуры "дерево", рассмотренный на уроке.
Предложите варианты доработки и оптимизации (например, валидация значений узлов
в соответствии с требованиями для бинарного дерева).
Поработайте с доработанной структурой, позапускайте на реальных данных -
на клиентском коде."""

"""Вариант 2.
Обеспечиваем корректность формирования бинарного дерева в методах класса, 
а также добавляем красивый вывод дерева (реализация позаимствована с небольшими 
адаптациями с ресурса StackOverflow: https://stackoverflow.com/questions/
34012886/print-binary-tree-level-by-level-in-python)"""


class BinaryTree:
    """Класс 'Двоичное дерево'"""

    def __init__(self, root_obj):
        self.root = root_obj     # корень
        self.left_child = None   # левый потомок
        self.right_child = None  # правый потомок

    def insert_child(self, new_node):
        """Добавление потомка"""

        if new_node >= self.root:
            # вставлять нужно в правую часть
            if self.right_child is None:
                # правого потомка еще нет - добавляем новое поддерево
                self.right_child = BinaryTree(new_node)
            else:
                # правый потомок уже есть - передаем вставку его методу
                self.right_child.insert_child(new_node)
        else:
            # вставлять нужно в левую часть (new_node < self.root)
            if self.left_child is None:
                # левого потомка еще нет - добавляем новое поддерево
                self.left_child = BinaryTree(new_node)
            else:
                # левый потомок уже есть - передаем вставку его методу
                self.left_child.insert_child(new_node)

    def get_left_child(self):
        """метод доступа к левому потомку"""
        return self.left_child

    def get_right_child(self):
        """метод доступа к правому потомку"""
        return self.right_child

    def get_root_val(self):
        """метод доступа к корню"""
        return self.root

    def display(self):
        """метод вывода на печать структуры дерева"""
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """возвращает список строк, ширину, высоту и позицию корня в строке"""

        S_CON = ' '  # заполнитель своб. пространства
        H_CON = '_'  # горизонтальный соединитель
        # вертикальные соединители (левый и правый - с экранир. символа)
        V_L_CON, V_R_CON = '/', '\\'

        # если потомков нет
        if self.right_child is None and self.left_child is None:
            line = f'{self.root}'
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # если только левый потомок
        if self.right_child is None:
            lines, width, height, middle = self.left_child._display_aux()
            root = f'{self.root}'
            l_root = len(root)
            first_line = (middle + 1) * S_CON + \
                         (width - middle - 1) * H_CON + root
            second_line = middle * S_CON + V_L_CON + \
                          (width - middle - 1 + l_root) * S_CON
            shifted_lines = [line + l_root * S_CON for line in lines]
            return [first_line, second_line] + shifted_lines, width + l_root, \
                   height + 2, width + l_root // 2

        # если только правый потомок
        if self.left_child is None:
            lines, width, height, middle = self.right_child._display_aux()
            root = f'{self.root}'
            l_root = len(root)
            first_line = root + middle * H_CON + (width - middle) * S_CON
            second_line = (l_root + middle) * S_CON + V_R_CON + \
                          (width - middle - 1) * S_CON
            shifted_lines = [l_root * S_CON + line for line in lines]
            return [first_line, second_line] + shifted_lines, width + l_root, \
                   height + 2, l_root // 2

        # если есть оба потомка
        left, l_width, l_height, l_middle = self.left_child._display_aux()
        right, r_width, r_height, r_middle = self.right_child._display_aux()
        root = f'{self.root}'
        l_root = len(root)
        first_line = (l_middle + 1) * S_CON + (l_width - l_middle - 1) * H_CON \
                     + root + r_middle * H_CON + (r_width - r_middle) * S_CON
        second_line = l_middle * S_CON + V_L_CON + \
                      (l_width - l_middle - 1 + l_root + r_middle) * S_CON \
                      + V_R_CON + (r_width - r_middle - 1) * S_CON
        if l_height < r_height:
            left += [l_width * S_CON] * (r_height - l_height)
        elif r_height < l_height:
            right += [r_width * S_CON] * (l_height - r_height)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + \
                [a + l_root * S_CON + b for a, b in zipped_lines]
        return lines, l_width + r_width + l_root, \
               max(l_height, r_height) + 2, l_width + l_root // 2


if __name__ == "__main__":

    test_tree = BinaryTree(50)
    for _ in range(50):
        test_tree.insert_child(randint(0, 100))
    test_tree.display()
