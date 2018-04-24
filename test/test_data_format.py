from benedict.data_format import *


D = OrderedDict(
    [('z','y'), ('x','w'), ('a', 'b'), ('c', 'd')]
)


def test_yaml():
    print(ordered_dumps_yaml(D))
    print(loads_yaml(ordered_dumps_yaml(D)))
    assert ordered_loads_yaml(ordered_dumps_yaml(D)) == D
    fpath = '~/Temp/ordered.yml'
    ordered_dump_yaml(D, fpath)
    print(load_yaml(fpath))
    assert ordered_load_yaml(fpath) == D


def test_json():
    print(ordered_dumps_yaml(D))
    print(loads_yaml(ordered_dumps_yaml(D)))
    assert ordered_loads_yaml(ordered_dumps_yaml(D)) == D
    fpath = '~/Temp/ordered.json'
    ordered_dump_yaml(D, fpath)
    print(load_yaml(fpath))
    assert ordered_load_yaml(fpath) == D
