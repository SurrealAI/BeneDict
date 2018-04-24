"""
JSON, YAML, and python config file utilities
"""
import json
import yaml
from io import StringIO
import os.path as path
from collections import OrderedDict
from functools import partial


def load_json_file(file_path, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, 'r') as fp:
        return json.load(fp, **kwargs)


def load_json_str(string, **kwargs):
    return json.loads(string, **kwargs)


def dump_json_file(data, file_path, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, 'w') as fp:
        indent = kwargs.get('indent', 4)
        json.dump(data, fp, indent=indent, **kwargs)


def dump_json_str(data, **kwargs):
    "Returns: string"
    return json.dumps(data, **kwargs)


ordered_load_json_file = partial(load_json_file, object_pairs_hook=OrderedDict)
ordered_load_json_str = partial(load_json_str, object_pairs_hook=OrderedDict)
ordered_dump_json_file = dump_json_file
ordered_dump_json_str = dump_json_str


def load_yaml_file(file_path, *, loader=yaml.load, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, 'r') as fp:
        return loader(fp, **kwargs)


def load_yaml_str(string, *, loader=yaml.load, **kwargs):
    return loader(string, **kwargs)


def dump_yaml_file(data, file_path, *, dumper=yaml.dump, **kwargs):
    file_path = path.expanduser(file_path)
    indent = kwargs.get('indent', 2)
    default_flow_style = kwargs.get('default_flow_style', False)
    with open(file_path, 'w') as fp:
        dumper(
            data,
            stream=fp,
            indent=indent,
            default_flow_style=default_flow_style,
            **kwargs
        )


def dump_yaml_str(data, *, dumper=yaml.dump, **kwargs):
    "Returns: string"
    stream = StringIO()
    indent = kwargs.get('indent', 2)
    default_flow_style = kwargs.get('default_flow_style', False)
    dumper(
        data,
        stream,
        indent=indent,
        default_flow_style=default_flow_style,
        **kwargs
    )
    return stream.getvalue()


def _ordered_load_stream_yaml(stream,
                              Loader=yaml.Loader,
                              object_pairs_hook=OrderedDict):
    """
    https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
    """
    class OrderedLoader(Loader):
        pass
    def _construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_mapping)
    return yaml.load(stream, OrderedLoader)


def _ordered_dump_stream_yaml(data, stream=None, Dumper=yaml.Dumper, **kwargs):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwargs)


ordered_load_yaml_file = partial(load_yaml_file, loader=_ordered_load_stream_yaml)
ordered_load_yaml_str = partial(load_yaml_str, loader=_ordered_load_stream_yaml)
ordered_dump_yaml_file = partial(dump_yaml_file, dumper=_ordered_dump_stream_yaml)
ordered_dump_yaml_str = partial(dump_yaml_str, dumper=_ordered_dump_stream_yaml)

