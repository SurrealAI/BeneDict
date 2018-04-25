import pytest
import pickle
from benedict import *
import sys


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


ORDERED_TESTDICT = OrderedDict(TESTDICT)


class MyDict(BeneDict):
    def show_config(self):
        print('MyDict method', self.to_dict())


class MyOrderedDict(OrderedBeneDict):
    def show_config(self):
        print('MyOrderedDict method', self.to_dict())


@pytest.fixture(params=[BeneDict, OrderedBeneDict, MyDict, MyOrderedDict])
def Dtype(request):
    """
    https://docs.pytest.org/en/latest/fixture.html
    """
    return request.param


@pytest.fixture(params=[OrderedBeneDict, MyOrderedDict])
def OrderedDtype(request):
    """
    https://docs.pytest.org/en/latest/fixture.html
    """
    return request.param


def test_1(Dtype):
    a = Dtype({'keys': Dtype({'items': 100, 'get': 66, 'update': 77})})
    b = a.deepcopy()
    b.keys.items = 120
    assert a.keys.items == 100
    assert a.keys.update == 77
    with pytest.raises(ValueError):
        Dtype({'keys': Dtype({'builtin_items': 100, 'get': 66})})


def test_2(Dtype):
    a = Dtype({'keys2': {'items2': 100, 'get2': 66, 'values':10}})
    b = a.deepcopy()
    b.keys2.items2 = 120
    aib = pickle.dumps(b)
    aib = pickle.loads(aib)
    print(aib)
    print(aib.keys2.get2)


def test_big(Dtype):
    D = Dtype(TESTDICT)
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
    D = MyDict(TESTDICT)
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


def test_deepcopy(Dtype):
    D = Dtype(TESTDICT)
    D_copy = D.deepcopy()
    D_copy.b0._a1 = 'changed'
    assert D.b0._a1 == 108


def test_json(Dtype):
    """
    Warning: JSON keys must be strings
    """
    JSON_TESTDICT = {
        'a0': [
            {'a1': 2},
            {'b1': 3},
            {'c1': 6},
        ],
        'b0': {
            'c1': [
                {'a2': 11},
                {'b2': 13},
            ],
            'd1': {'e2': 100},
            '*&': {'e2': 104},
            '_a1': 108
        },
        '0c': 200,
    }
    D = Dtype(JSON_TESTDICT)
    file_path = '~/Temp/test.json'
    D.dump_file(file_path)
    D_loaded = Dtype.load_file(file_path)
    assert D == D_loaded


def test_yaml(Dtype):
    D = Dtype(TESTDICT)
    file_path = '~/Temp/test.yml'
    D.dump_file(file_path)
    D_loaded = Dtype.load_file(file_path)
    assert D == D_loaded


def test_ordered_insert(Dtype):
    """
    Notes:
        Python 3.6, all dict insertion order is guaranteed,
            vanilla BeneDict will also pass this test
        Python 3.5, only OrderedBeneDict will pass this test
        Python 3.4 will simply crash due to OrderedDict internal problem
    """
    D = Dtype()
    O = OrderedDict()
    nums = [10, 7, 2, 8, 4, 1, 3, 9, 5, 6]

    for i in nums:
        key = 'k{}'.format(i)
        O[key] = i
        setattr(D, key, i)

    D_items = list(D.to_dict().items())
    O_items = list(O.items())

    if (Dtype in [OrderedBeneDict, MyOrderedDict]
        or sys.version_info.minor >= 6):  # py 3.6 order guaranteed
        print(D_items)
        assert D_items == O_items


