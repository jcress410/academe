from pyramid.request import Request
from pyramid.registry import Registry


def new_dbsession(obj, name=''):
    if isinstance(obj, Request):
        return new_dbsession(request.registry.settings, name)
    elif isinstance(obj, registry):
        return new_dbsession(registry.settings, name)
    elif isinstance(obj, dict):
        key = 'academe.db_session_factory'
        if name:
            key = name + '_' + key
        return obj[key]()
    raise TypeError('Cannot retrieve session from %s' % str(type(obj)))
