import pickle, traceback
from benedict import (
    _print_protected_methods, BeneDict
)


_print_protected_methods()


TESTDICT = {
    'a0': [
        {'a1': 2},
        {'b1': 3},
        {'c1': 6},
        {'?': 7}
    ],
    'b0': {
        'c1': [
            {'a2': 11},
            {'b2': 13},
            {-13: 'yo'},
            {-15: {'a3': 'yo'}},
            15
        ],
        'd1': {'e2': 100},
        '*&': {'e2': 104},
        -10: {'e2': 106},
        '_a1': 108
    },
    '0c': 200,
    -1.3: 'yo'
}


class MyClass(BeneDict):
    a0 = [
        {'a1': 2},
        {'b1': 3},
        {'c1': 6},
        {'?': 7}
    ]
    b0 = {
        'c1': [
            {'a2': 11},
            {'b2': 13},
            {-13: 'yo'},
            {-15: {'a3': 'yo'}},
            15
        ],
        'd1': {'e2': 100},
        '*&': {'e2': 104},
        -10: {'e2': 106},
        '_a1': 108
    }
    _c0 = (200, 300, 400)


class TestBuiltin(BeneDict):
    keys = (20, 30)
    items = 5
    get = 8
    a1 = 10


def test_1():
    a = BeneDict({'keys': BeneDict({'items': 100, 'get': 66, 'builtin_items': 'bad'})})
    b = a.deepcopy()
    b.keys.items = 120
    print(a.keys.builtin_items())
    print(b.keys)
    print(b.keys.get)
    # aib = pickle.dumps(b)
    # aib = pickle.loads(aib)
    # print(aib)
    # print(aib.keys)


def test_2():
    a = BeneDict({'keys2': {'items2': 100, 'get2': 66, 'values':10}})
    b = a.deepcopy()
    b.keys2.items2 = 120
    aib = pickle.dumps(b)
    aib = pickle.loads(aib)
    print(aib)
    print(aib.keys2.get2)


def test_big():
    D = BeneDict(TESTDICT)
    assert D.a0[0].a1 == 2
    assert D.b0.c1[0].a2 == 11
    assert D.b0.c1[1].b2 == 13
    assert D.a0[-1]['?'] == 7
    assert D.b0['*&'].e2 == 104
    assert D['0c'] == 200
    assert D[-1.3] == 'yo'
    assert D.b0.c1[2][-13] == 'yo'
    assert D.b0.c1[3][-15].a3 == 'yo'
    assert D.b0[-10].e2 == 106
    assert D.b0._a1 == 108


def test_myclass():
    D = MyClass()
    assert D.a0[0].a1 == 2
    assert D.b0.c1[0].a2 == 11
    assert D.b0.c1[1].b2 == 13
    assert D.a0[-1]['?'] == 7
    assert D.b0['*&'].e2 == 104
    assert D._c0 == (200, 300, 400)
    assert D.b0.c1[2][-13] == 'yo'
    assert D.b0.c1[3][-15].a3 == 'yo'
    assert D.b0[-10].e2 == 106
    assert D.b0._a1 == 108


def test_builtin_inherit():
    D = TestBuiltin()
    assert D.keys == (20, 30)
    assert D.items == 5
    assert D.a1 == 10

# test_1()
# test_2()
test_big()
test_myclass()
test_builtin_inherit()
