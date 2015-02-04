__author__ = 'Excelle'

mysql_dbhost = '127.0.0.1'
mysql_username = 'root'
mysql_password = 'zgsdzlx'
mysql_database = 'awesome'

import config_default


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for key, value in zip(names, values):
            self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError("'Dict' object has no attribute %s" % item)

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    r = {}
    for k, v in defaults.iteritems():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def toDict(d):
    D = Dict()
    for k,v in d.iteritems():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)