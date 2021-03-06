from persistent.mapping import PersistentMapping
from persistent import Persistent


class Academic(PersistentMapping):
    __parent__ = __name__ = None


class UserInfo(Persistent):
    def__init__(self, name):


class Blog(Persistent):
    pass

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Academic()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
