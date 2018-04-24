"""
JSON, YAML, and python config file utilities
"""
import json
import yaml
from io import StringIO
import os.path as path
from collections import OrderedDict
from functools import partial


def load_json(file_path, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, 'r') as fp:
        return json.load(fp, **kwargs)


def loads_json(string, **kwargs):
    return json.loads(string, **kwargs)


def dump_json(data, file_path, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, 'w') as fp:
        indent = kwargs.get('indent', 4)
        json.dump(data, fp, indent=indent, **kwargs)


def dumps_json(data, **kwargs):
    "Returns: string"
    return json.dumps(data, **kwargs)


ordered_load_json = partial(load_json, object_pairs_hook=OrderedDict)
ordered_loads_json = partial(loads_json, object_pairs_hook=OrderedDict)
ordered_dump_json = dump_json
ordered_dumps_json = dumps_json


def load_yaml(file_path, *, loader=yaml.load, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, 'r') as fp:
        return loader(fp, **kwargs)


def loads_yaml(string, *, loader=yaml.load, **kwargs):
    return loader(string, **kwargs)


def dump_yaml(data, file_path, *, dumper=yaml.dump, **kwargs):
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


def dumps_yaml(data, *, dumper=yaml.dump, **kwargs):
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


ordered_load_yaml = partial(load_yaml, loader=_ordered_load_stream_yaml)
ordered_loads_yaml = partial(loads_yaml, loader=_ordered_load_stream_yaml)
ordered_dump_yaml = partial(dump_yaml, dumper=_ordered_dump_stream_yaml)
ordered_dumps_yaml = partial(dumps_yaml, dumper=_ordered_dump_stream_yaml)
