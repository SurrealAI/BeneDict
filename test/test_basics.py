import pytest
import pickle
from benedict import (
    _print_protected_methods, BeneDict
)


# _print_protected_methods()


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


class ConfigDict(BeneDict):
    def show_config(self):
        print('ConfigDict method', self.to_dict())


def test_1():
    a = BeneDict({'keys': BeneDict({'items': 100, 'get': 66, 'update': 77})})
    b = a.deepcopy()
    b.keys.items = 120
    assert a.keys.items == 100
    assert a.keys.update == 77
    with pytest.raises(ValueError):
        BeneDict({'keys': BeneDict({'builtin_items': 100, 'get': 66})})


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
    D = ConfigDict(TESTDICT)
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
    D.b0.show_config()
    D.b0.show_config = 'overriden'
    D.b0.builtin_show_config()
    with pytest.raises(ValueError):
        D.b0.builtin_show_config = 'overriden'


