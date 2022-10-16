""" Задание 8.2. Доработайте пример структуры "дерево", рассмотренный на уроке.
Предложите варианты доработки и оптимизации (например, валидация значений узлов
в соответствии с требованиями для бинарного дерева).
Поработайте с доработанной структурой, позапускайте на реальных данных -
на клиентском коде."""

"""Вариант 1.
Создаем свое исключение и поднимаем его при нарушении правила двоичного дерева 
поиска (потомок слева должен быть меньше корня, а справа - больше или равен)"""


class BinaryTree:
    """Класс 'Двоичное дерево'"""
    def __init__(self, root_obj):
        self.root = root_obj     # корень
        self.left_child = None   # левый потомок
        self.right_child = None  # правый потомок

    def set_root_val(self, new_root):
        """метод установки корня"""
        if self.left_child is not None and self.left_child >= new_root:
            raise BinaryTreeError(msg=f'Новый корень: {new_root} должен быть '
                                      f'больше, чем левый потомок: '
                                      f'{self.left_child}')
        if self.right_child is not None and self.right_child < new_root:
            raise BinaryTreeError(msg=f'Новый корень: {new_root} должен быть '
                                      f'меньше или равен правого потомка: '
                                      f'{self.right_child}')
        self.root = new_root

    def insert_left(self, new_node):
        """Добавление левого потомка"""

        # проверяем соблюдение правила двоичного дерева
        if (self.left_child is None and new_node >= self.root) or \
                (self.left_child is not None and
                 self.left_child >= new_node >= self.root):
            raise BinaryTreeError(msg=f'Левый потомок: "{new_node}" - '
                                      f'не должен быть больше или равен '
                                      f'корню: "{self.root}"')
        if self.left_child is None:
            # если у узла нет левого потомка - просто вставляем узел
            # в дерево и формируем новое поддерево
            self.left_child = BinaryTree(new_node)
        else:
            # если у узла есть левый потомок (не None) - вставляем новый узел
            tree_obj = BinaryTree(new_node)
            # и спускаем имеющегося потомка на один уровень ниже
            tree_obj.left_child = self.left_child
            self.left_child = tree_obj

    def insert_right(self, new_node):
        """Добавление правого потомка"""

        # проверяем соблюдение правила двоичного дерева
        if self.left_child is None:
            raise BinaryTreeError(msg='Нельзя добавлять правого потомка, пока '
                                      'не заполнен левый потомок!')

        if (self.right_child is None and new_node < self.root) or \
                (self.right_child is not None and
                 self.right_child < new_node < self.root):
            raise BinaryTreeError(msg=f'Правый потомок: "{new_node}" - '
                                      f'не должен быть меньше корня: '
                                      f'"{self.root}"')

        if self.right_child is None:
            # если у узла нет правого потомка - просто вставляем узел
            # в дерево и формируем новое поддерево
            self.right_child = BinaryTree(new_node)
        else:
            # если у узла есть правый потомок (не None) - вставляем новый узел
            tree_obj = BinaryTree(new_node)
            # и спускаем имеющегося потомка на один уровень ниже
            tree_obj.right_child = self.right_child
            self.right_child = tree_obj

    def get_left_child(self):
        """метод доступа к левому потомку"""
        return self.left_child

    def get_right_child(self):
        """метод доступа к правому потомку"""
        return self.right_child

    def get_root_val(self):
        """метод доступа к корню"""
        return self.root


class BinaryTreeError(Exception):
    """Класс ошибки правил бинарного дерева"""

    def __init__(self, msg=None, *args, **kwargs):
        self.message = msg  # сообщение об ошибке

    def __str__(self):
        res = f'{self.__class__.__name__} has been raised'
        # если передано сообщение - добавляем его к строке ошибки
        return (res + f': {self.message}') if self.message else res


if __name__ == "__main__":

    print('Создаем дерево с корнем 8')
    test_tree = BinaryTree(8)
    print(f'Получаем корень: {test_tree.get_root_val()=}')
    print(f'Получаем левого потомка: {test_tree.get_left_child()=}')

    print('\nПробуем добавить левого потомка 40')
    try:
        test_tree.insert_left(40)
    except BinaryTreeError as err:
        print(f'Возникло исключение в связи с нарушением правил бинарного '
              f'дерева: {err}')
    else:
        print(f'Левый потомок: {test_tree.get_left_child()=}')
        print(f'Получаем корень левого потомка: '
              f'{test_tree.get_left_child().get_root_val()=}')

    print('\nПробуем добавить правого потомка 12')
    try:
        test_tree.insert_right(12)
    except BinaryTreeError as err:
        print(f'Возникло исключение в связи с нарушением правил бинарного '
              f'дерева: {err}')
    else:
        print(f'Правый потомок: {test_tree.get_right_child()=}')
        print(f'Получаем корень правого потомка: '
              f'{test_tree.get_right_child().get_root_val()=}')

    print('\nПробуем установить значение корня 16 для правого потомка')
    try:
        test_tree.get_right_child().set_root_val(16)
    except AttributeError as err:
        print(f'Возникло исключение при установке значения корня: {err}')
    except BinaryTreeError as err:
        print(f'Возникло исключение в связи с нарушением правил бинарного '
              f'дерева: {err}')
    else:
        print(f'{test_tree.get_right_child().get_root_val()=}')
