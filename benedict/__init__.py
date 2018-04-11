"""
BeneDict enables accessing dict values by attribute, just like Javascript's
dot notation. Supports JSON/YAML operations.
Builtin methods like "values()" and "items()" can be overriden by the data keys,
but their original version will always be protected with prefix builtin_

Adapted from: https://github.com/makinacorpus/EasyDict
"""
import json
import yaml
from io import StringIO
from os.path import expanduser


def _get_special_methods():
    methods = ['keys', 'items', 'values', 'get', 'clear',
               'update', 'pop', 'popitem',
               'to_dict', 'deepcopy']
    for action in ['load', 'dump']:
        for mode in ['s', '']:  # 's' for string, '' for file
            for format in ['json', 'yaml']:
                methods.append(action + mode + '_' + format)
    protected = ['builtin_' + m for m in methods]
    return methods + protected, protected


_BeneDict_NATIVE_METHODS, _BeneDict_PROTECTED_METHODS = _get_special_methods()


class BeneDict(dict):
    """
    BeneDict enables accessing dict values by attribute, just like Javascript's
    dot notation. Supports JSON/YAML operations.

    Adapted from: https://github.com/makinacorpus/EasyDict

    Notes:
      Use `dict.items()` if you know there might be conflict in the keys
      or `builtin_` + method name

    Added methods: the version always prefixed by `builtin` is protected against
      changes. You can use the non-prefixed version if you know for sure that
      the name will never be overriden

    >>> d = BeneDict({'foo':3})
    >>> d['foo']
    3
    >>> d.foo
    3
    >>> d.bar
    Traceback (most recent call last):
    ...
    AttributeError: 'BeneDict' object has no attribute 'bar'

    Works recursively

    >>> d = BeneDict({'foo':3, 'bar':{'x':1, 'y':2}})
    >>> isinstance(d.bar, dict)
    True
    >>> d.bar.x
    1

    Bullet-proof

    >>> BeneDict({})
    {}
    >>> BeneDict(d={})
    {}
    >>> BeneDict(None)
    {}
    >>> d = {'a': 1}
    >>> BeneDict(**d)
    {'a': 1}

    Set attributes

    >>> d = BeneDict()
    >>> d.foo = 3
    >>> d.foo
    3
    >>> d.bar = {'prop': 'value'}
    >>> d.bar.prop
    'value'
    >>> d
    {'foo': 3, 'bar': {'prop': 'value'}}
    >>> d.bar.prop = 'newer'
    >>> d.bar.prop
    'newer'


    Values extraction

    >>> d = BeneDict({'foo':0, 'bar':[{'x':1, 'y':2}, {'x':3, 'y':4}]})
    >>> isinstance(d.bar, list)
    True
    >>> from operator import attrgetter
    >>> map(attrgetter('x'), d.bar)
    [1, 3]
    >>> map(attrgetter('y'), d.bar)
    [2, 4]
    >>> d = BeneDict()
    >>> d.keys()
    []
    >>> d = BeneDict(foo=3, bar=dict(x=1, y=2))
    >>> d.foo
    3
    >>> d.bar.x
    1

    Still like a dict though

    >>> o = BeneDict({'clean':True})
    >>> o.items()
    [('clean', True)]

    And like a class

    >>> class Flower(BeneDict):
    ...     power = 1
    ...
    >>> f = Flower()
    >>> f.power
    1
    >>> f = Flower({'height': 12})
    >>> f.height
    12
    >>> f['power']
    1
    >>> sorted(f.keys())
    ['height', 'power']
    """
    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        if kwargs:
            dict.update(d, **kwargs)
        for k, v in dict.items(d):
            setattr(self, k, v)
        # Class attributes
        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')
                    or k in _BeneDict_NATIVE_METHODS):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if name in _BeneDict_PROTECTED_METHODS:
            raise ValueError('Cannot override `{}`: BeneDict protected method'
                             .format(name))
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict):
            # implements deepcopy if BeneDict(BeneDict())
            # to make it shallow copy, add the following condition:
            # ...  and not isinstance(value, self.__class__)):
            value = self.__class__(value)
        super(BeneDict, self).__setattr__(name, value)
        super(BeneDict, self).__setitem__(name, value)

    __setitem__ = __setattr__

    def to_dict(self):
        """
        Convert to raw dict
        """
        return ezdict_to_dict(self)

    def deepcopy(self):
        return BeneDict(self)

    @classmethod
    def load_json(cls, file_path):
        file_path = expanduser(file_path)
        with open(file_path, 'r') as fp:
            return cls(json.load(fp))

    @classmethod
    def loads_json(cls, string):
        return cls(json.loads(string))

    @classmethod
    def load_yaml(cls, file_path):
        file_path = expanduser(file_path)
        with open(file_path, 'r') as fp:
            return cls(yaml.load(fp))

    @classmethod
    def loads_yaml(cls, string):
        return cls(yaml.load(string))

    def dump_json(self, file_path):
        file_path = expanduser(file_path)
        with open(file_path, 'w') as fp:
            json.dump(ezdict_to_dict(self), fp, indent=4)

    def dumps_json(self):
        "Returns: string"
        return json.dumps(ezdict_to_dict(self))

    def dump_yaml(self, file_path):
        file_path = expanduser(file_path)
        with open(file_path, 'w') as fp:
            yaml.dump(
                ezdict_to_dict(self),
                stream=fp,
                indent=2,
                default_flow_style=False
            )

    def dumps_yaml(self):
        "Returns: string"
        stream = StringIO()
        yaml.dump(
            ezdict_to_dict(self),
            stream,
            default_flow_style=False,
            indent=2
        )
        return stream.getvalue()

    def __getstate__(self):
        """
        Support pickling.
        Warning:
          if this BeneDict overrides dict builtin methods, like `items`,
          pickle will report error.
          don't know how to resolve yet
        """
        return self.builtin_to_dict()

    def __setstate__(self, state):
        self.__init__(state)

    def __str__(self):
        return str(ezdict_to_dict(self))

    builtin_keys = dict.keys
    builtin_items = dict.items
    builtin_values = dict.values
    builtin_get = dict.get
    builtin_clear = dict.clear
    builtin_update = dict.update
    builtin_pop = dict.pop
    builtin_popitem = dict.popitem
    builtin_to_dict = to_dict
    builtin_deepcopy = deepcopy
    builtin_loads_json = loads_json
    builtin_loads_yaml = loads_yaml
    builtin_load_json = load_json
    builtin_load_yaml = load_yaml
    builtin_dumps_json = dumps_json
    builtin_dumps_yaml = dumps_yaml
    builtin_dump_json = dump_json
    builtin_dump_yaml = dump_yaml


def ezdict_to_dict(easy_dict):
    """
    Recursively convert back to builtin dict type
    """
    d = {}
    for k, value in dict.items(easy_dict):
        if isinstance(value, BeneDict):
            d[k] = ezdict_to_dict(value)
        elif isinstance(value, (list, tuple)):
            d[k] = type(value)(
                ezdict_to_dict(v)
                if isinstance(v, BeneDict)
                else v for v in value
            )
        else:
            d[k] = value
    return d


def _add_protected_methods():
    for protected, normal in zip(_BeneDict_PROTECTED_METHODS,
                                 _BeneDict_NATIVE_METHODS):
        setattr(BeneDict, protected, getattr(BeneDict, normal))

_add_protected_methods()
