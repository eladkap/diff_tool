from diff import DiffTool
from constants import *


class B:
    def __init__(self, attr_c):
        self.attr_c = attr_c


class A:
    def __init__(self, attr_a, attr_b, attr_c):
        self.attr_a = attr_a
        self.attr_b = attr_b
        self.attr_c = attr_c


def primitive_test():
    diff_tool = DiffTool()
    assert diff_tool.is_primitive(6)
    assert diff_tool.is_primitive(False)
    assert diff_tool.is_primitive(5.5)
    assert diff_tool.is_primitive('qwerty')
    assert not diff_tool.is_primitive([1, 2, 'go'])
    assert not diff_tool.is_primitive({1, 2, 3})
    assert not diff_tool.is_primitive((1, 2, 3))
    assert not diff_tool.is_primitive({1: 'one', 2: 'two'})


def both_objects_none_test():
    diff_tool = DiffTool()
    changes = diff_tool.diff_objects(None, None)
    assert changes == [NOT_CHANGED]


def left_object_is_none_test():
    diff_tool = DiffTool()
    changes = diff_tool.diff_objects(None, 6)
    assert changes == [f'{TYPE_CHANGE}: NoneType -> int']


def right_object_is_none_test():
    diff_tool = DiffTool()
    changes = diff_tool.diff_objects([1, 2, 3], None)
    assert changes == [f'{TYPE_CHANGE}: list -> NoneType']


def both_objects_primitive_same_content():
    diff_tool = DiffTool()
    changes = diff_tool.diff_objects('hello', 'hello')
    assert changes == [NOT_CHANGED]


def both_objects_primitive_diff_content():
    diff_tool = DiffTool()
    changes = diff_tool.diff_objects('hello', 'world')
    assert changes == [f'{VALUE_CHANGE}: hello -> world']


def both_objects_primitive_diff_type():
    diff_tool = DiffTool()
    changes = diff_tool.diff_objects('hello', 5.6)
    assert changes == [f'{TYPE_CHANGE}: str -> float']


def diff_lists_tests():
    diff_tool = DiffTool()
    list1 = [1, 2, 'hello', 5.5]
    list2 = [1, 3, 'world', 'hi']
    changes = diff_tool.diff_objects(list1, list2)
    assert len(changes) == 5
    assert changes[0] == COMPLEX_CHANGE
    assert changes[1] == NOT_CHANGED
    assert changes[2] == f'{VALUE_CHANGE}: 2 -> 3'
    assert changes[3] == f'{VALUE_CHANGE}: hello -> world'
    assert changes[4] == f'{TYPE_CHANGE}: float -> str'


def diff_lists_complex_remove():
    diff_tool = DiffTool()
    list1 = [1, 2, [1, 'three', True], 5.5, 7]
    list2 = [1, 3, [2, 3, 'xxx'], 'hi']
    changes = diff_tool.diff_objects(list1, list2)
    assert len(changes) == 8
    assert changes[0] == COMPLEX_CHANGE
    assert changes[1] == NOT_CHANGED
    assert changes[2] == f'{VALUE_CHANGE}: 2 -> 3'
    assert changes[3] == COMPLEX_CHANGE
    assert changes[4] == f'{VALUE_CHANGE}: 1 -> 2'
    assert changes[5] == f'{TYPE_CHANGE}: str -> int'
    assert changes[6] == f'{TYPE_CHANGE}: bool -> str'
    assert changes[7] == f'{TYPE_CHANGE}: float -> str'
    assert changes[8] == f'{REMOVED_CHANGE}: 7'


def diff_lists_complex_add():
    diff_tool = DiffTool()
    list1 = [1, 2, [1, 'three', True], 5.5]
    list2 = [1, 3, [2, 3, 'xxx'], 'hi', 8]
    changes = diff_tool.diff_objects(list1, list2)
    assert len(changes) == 8
    assert changes[0] == COMPLEX_CHANGE
    assert changes[1] == NOT_CHANGED
    assert changes[2] == f'{VALUE_CHANGE}: 2 -> 3'
    assert changes[3] == COMPLEX_CHANGE
    assert changes[4] == f'{VALUE_CHANGE}: 1 -> 2'
    assert changes[5] == f'{TYPE_CHANGE}: str -> int'
    assert changes[6] == f'{TYPE_CHANGE}: bool -> str'
    assert changes[7] == f'{TYPE_CHANGE}: float -> str'
    assert changes[8] == f'{ADDED_CHANGE}: 8'


def example_test1():
    diff_tool = DiffTool()
    a_instance = A(attr_a=5, attr_b='dfdf', attr_c=B(attr_c=4))
    b_instance = A(attr_a=6, attr_b=5, attr_c=B(attr_c=5))
    changes = diff_tool.diff_objects(a_instance, b_instance)
    assert len(changes) == 5
    assert changes[0] == COMPLEX_CHANGE
    assert changes[1] == f'Attribute attr_a - {VALUE_CHANGE}: 5 -> 6'
    assert changes[2] == f'Attribute attr_b - {TYPE_CHANGE}: str -> int'
    assert changes[2] == f'Attribute attr_c - {COMPLEX_CHANGE}'
    assert changes[2] == f'Attribute attr_c - {VALUE_CHANGE}: 4 -> 5'


if __name__ == '__main__':
    primitive_test()
    both_objects_none_test()
    left_object_is_none_test()
    right_object_is_none_test()
    both_objects_primitive_same_content()
    both_objects_primitive_diff_content()
    both_objects_primitive_diff_type()
    diff_lists_tests()
    example_test1()
    # diff_lists_complex_add()
    # diff_lists_complex_remove()
