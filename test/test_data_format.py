from benedict.data_format import *


D = OrderedDict(
    [('z','y'), ('x','w'), ('a', 'b'), ('c', 'd')]
)


def test_yaml():
    print(ordered_dump_yaml_str(D))
    print(load_yaml_str(ordered_dump_yaml_str(D)))
    assert ordered_load_yaml_str(ordered_dump_yaml_str(D)) == D
    fpath = '~/Temp/ordered.yml'
    ordered_dump_yaml_file(D, fpath)
    print(load_yaml_file(fpath))
    assert ordered_load_yaml_file(fpath) == D


def test_json():
    print(ordered_dump_json_str(D))
    print(load_json_str(ordered_dump_json_str(D)))
    assert ordered_load_json_str(ordered_dump_json_str(D)) == D
    fpath = '~/Temp/ordered.json'
    ordered_dump_json_file(D, fpath)
    print(load_json_file(fpath))
    assert ordered_load_json_file(fpath) == D

