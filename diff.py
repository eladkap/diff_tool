from constants import *


class DiffTool:
    def __init__(self):
        pass

    def is_primitive(self, obj) -> bool:
        return type(obj) in PRIMITIVE_TYPES or obj is None

    def have_same_type(self, old_object: object, new_object: object) -> bool:
        return type(old_object) == type(new_object)

    def diff_primitives(self, old_object, new_object, attribute, level) -> str:
        if not self.have_same_type(old_object, new_object):
            return f"{' ' * level * 2}- Attribute: {attribute} - {TYPE_CHANGE}: {type(old_object).__name__} -> {type(new_object).__name__}"
        if old_object == new_object:
            return f"{' ' * level * 2}- Attribute: {attribute} - {NOT_CHANGED}"
        else:
            return f"{' ' * level * 2}- Attribute: {attribute} - {VALUE_CHANGE}: {old_object} -> {new_object}"

    def convert_object_to_dictionary(self, obj):
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, list) or isinstance(obj, tuple):
            return {i: obj[i] for i in range(len(obj))}
        elif isinstance(obj, set):
            return {x: x for x in obj}
        else:
            attributes = [a for a in dir(obj) if not a.startswith('__')]
            return {attr: obj.__getattribute__(attr) for attr in attributes}

    def diff_objects(self, old_object, new_object) -> list:
        changes = []
        self.diff_objects_aux(old_object, new_object, 'object', 0, changes)
        return changes

    def diff_objects_aux(self, old_object, new_object, attribute, level, changes):
        # Objects are not the same type
        if not self.have_same_type(old_object, new_object):
            changes.append(
                f"{' ' * level * 2}- Attribute: {attribute} - {TYPE_CHANGE}: {type(old_object).__name__} -> {type(new_object).__name__}")
            return

        # Primitive objects
        if self.is_primitive(old_object):
            changes.append(self.diff_primitives(old_object, new_object, attribute, level))
            return

        # Complex objects
        changes.append(f"{' ' * level * 2}- Attribute {attribute} - {COMPLEX_CHANGE}")

        # Convert object to dictionary (object can be list/tuple/set/class/dictionary
        old_dict = self.convert_object_to_dictionary(old_object)
        new_dict = self.convert_object_to_dictionary(new_object)

        old_keys = list(old_dict.keys())
        new_keys = list(new_dict.keys())

        for old_attr in old_keys:
            if old_attr not in new_keys:
                changes.append(f"{' ' * level * 2}- Attribute {old_attr} - {REMOVED_CHANGE}: {old_dict[old_attr]}")

        for new_attr in new_keys:
            if new_attr not in old_keys:
                changes.append(f"{' ' * level * 2}- Attribute {new_attr} - {ADDED_CHANGE}: {new_dict[new_attr]}")

        for attr in old_keys:
            if attr in new_keys:
                self.diff_objects_aux(old_dict[attr], new_dict[attr], attr, level + 1, changes)
