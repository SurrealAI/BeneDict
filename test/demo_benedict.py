import pickle, traceback
from benedict import (
    _BeneDict_NATIVE_METHODS, _BeneDict_PROTECTED_METHODS, BeneDict
)


def _print_protected_methods():
    "paste the generated code into BeneDict class for PyCharm convenience"
    for i, (protected, normal) in enumerate(zip(_BeneDict_PROTECTED_METHODS,
                                                _BeneDict_NATIVE_METHODS)):
        if i < 8:
            normal = 'dict.' + normal
        print('{} = {}'.format(protected, normal))


_print_protected_methods()
if 1:
    a = BeneDict({'keys': BeneDict({'items': 100, 'get': 66})})
    b = a.deepcopy()
    b.keys.items = 120
    print(a.keys.builtin_items())
    print(b.keys)
    print(b.keys.get)
    # aib = pickle.dumps(b)
    # aib = pickle.loads(aib)
    # print(aib)
    # print(aib.keys)
else:
    a = BeneDict({'keys2': {'items2': 100, 'get2': 66, 'values':10}})
    b = a.deepcopy()
    b.keys2.items2 = 120
    aib = pickle.dumps(b)
    aib = pickle.loads(aib)
    print(aib)
    print(aib.keys2.get2)
