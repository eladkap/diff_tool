from diff import DiffTool


class B:
    def __init__(self, attr_c):
        self.attr_c = attr_c


class A:
    def __init__(self, attr_a, attr_b, attr_c):
        self.attr_a = attr_a
        self.attr_b = attr_b
        self.attr_c = attr_c


if __name__ == '__main__':
    diff_tool = DiffTool()
    a_instance = A(attr_a=5, attr_b='dfdf', attr_c=B(attr_c=4))
    b_instance = A(attr_a=6, attr_b=5, attr_c=B(attr_c=5))
    changes = diff_tool.diff_objects(a_instance, b_instance)

    for change in changes:
        print(change)


    list1 = [1, 2, [1, 'three', a_instance], 5.5, 7]
    list2 = [1, 3, [2, 3, b_instance], 'hi']
    changes = diff_tool.diff_objects(list1, list2)

    for change in changes:
        print(change)

    list1 = [1, 2, [1, 'three', True], 5.5]
    list2 = [1, 3, [2, 3, 'xxx'], 'hi', 8]
    changes = diff_tool.diff_objects(list1, list2)

    for change in changes:
        print(change)
