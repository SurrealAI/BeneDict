import re
from benedict.core import BeneDict


class ConfigError(Exception):
    pass


def _trace_key(dict_trace, key):
    return 'key "{}" '.format('.'.join(dict_trace + [key]))


_enum_marker = re.compile('_enum\[(.*)\]_')


def _req_type_check(value):
    if not isinstance(value, str):
        return None
    value = value.lower()
    if value == '_object_':
        return lambda x: True
    elif value == '_singleton_':
        return lambda x: not isinstance(x, (list, dict))  # non-collection
    elif value == '_list_':
        return lambda x: isinstance(x, list)
    elif value == '_dict_':
        return lambda x: isinstance(x, dict)
    elif value == '_int_':
        return lambda x: isinstance(x, int)
    elif value == '_float_':
        return lambda x: isinstance(x, float)
    elif value == '_num_':
        return lambda x: isinstance(x, (int, float))
    elif value == '_str_':
        return lambda x: isinstance(x, str)
    elif value == '_bool_':
        return lambda x: isinstance(x, bool)
    elif _enum_marker.match(value):
        enum_options = _enum_marker.match(value).group(1)
        if not enum_options:
            raise ConfigError('_enum[...]_ cannot be empty')
        enum_options = list(map(str.strip, enum_options.split(',')))
        return lambda x: x in enum_options
    else:
        return None


def _is_req(value):
    return _req_type_check(value) is not None


def _has_req(config):
    for key, val in config.items():
        if _is_req(val):
            return True
        elif isinstance(val, dict):
            if _has_req(val):
                return True
    return False


def _raise_req_error(key, value, dict_trace, prefix_msg=''):
    value = value.lower()
    if value == '_object_':
        msg = 'filled'
    elif value == '_singleton_':
        msg = 'a singleton (non-list/dict)'
    elif value == '_list_':
        msg = 'a list'
    elif value == '_dict_':
        msg = 'a dict'
    elif value == '_int_':
        msg = 'an integer'
    elif value == '_float_':
        msg = 'a float'
    elif value == '_num_':
        msg = 'a numeric value'
    elif value == '_str_':
        msg = 'a string'
    elif value == '_bool_':
        msg = 'a boolean'
    elif _enum_marker.match(value):
        enum_options = _enum_marker.match(value).group(1)
        msg = 'an enum in [{}]'.format(enum_options)
    else:
        assert False, 'internal error: req value fell through'
    prefix_msg = prefix_msg+' ' if prefix_msg else ''
    raise ConfigError('{}{}must be {}.'
                      .format(prefix_msg, _trace_key(dict_trace, key), msg))


def _fill_default_config(config, default_config, dict_trace):
    for key, default_value in default_config.items():
        if key not in config:
            if _is_req(default_value):
                _raise_req_error(key, default_value, dict_trace,
                                 'Required entry missing:')
            elif isinstance(default_value, dict):
                if _has_req(default_value):
                    raise ConfigError(
                        'Sub-dict under key "{}" contains a required config: {}.'
                        .format(_trace_key(dict_trace, key), default_value)
                    )
            config[key] = default_value
        else:
            value = config[key]
            if _is_req(default_value):
                # value remains a placeholder after being extended
                if _is_req(value):
                    if value != default_value:
                        raise ConfigError(
                            'inherited {}: "{}" must match default "{}"'
                            .format(_trace_key(dict_trace, key),
                                    value, default_value)
                        )
                else:
                    checker = _req_type_check(default_value)
                    if not checker(value):
                        _raise_req_error(
                            key, default_value, dict_trace, 'Wrong type:')
            else:
                if (isinstance(value, dict) and
                        not isinstance(default_value, dict)):
                    raise ConfigError(
                        _trace_key(dict_trace, key)
                        + 'must be a singleton instead of a sub-dict'
                    )
                if isinstance(default_value, dict):
                    if not isinstance(value, dict):
                        raise ConfigError(
                            _trace_key(dict_trace, key)
                            + 'must have a sub-dict instead of a singleton'
                        )
                    config[key] = _fill_default_config(
                        value,
                        default_value,
                        dict_trace + [key]
                    )
    return config


class Config(BeneDict):
    def __getattr__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            raise ConfigError('config key "{}" missing.'.format(key))

    def extend(self, default_config):
        assert isinstance(default_config, dict)
        return _fill_default_config(self, default_config, [])


def extend_config(config, default_config):
    """
    default_config must specify all the expected keys. Use the following special
    values for required placeholders:

    * _req_: require a single value (not a list or dict)
    * _req_DICT_: require a dict
    * _req_LIST_: require a list

    Returns:
        AttributeDict
        `config` filled by default values if certain keys are unspecified

    Raises:
        ConfigError if required placeholders are not satisfied
    """
    assert isinstance(config, dict)
    assert isinstance(default_config, dict)
    return Config(_fill_default_config(config, default_config, []))
