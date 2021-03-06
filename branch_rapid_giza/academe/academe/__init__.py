from academe.traversal import get_root

from pyramid.configuration import Configurator
from pyramid_jinja2 import renderer_factory
import sqlalchemy
from sqlalchemy import orm 
from repoze import tm
from zope.sqlalchemy import ZopeTransactionExtension


DEFAULT_CONNECT_STRING = 'sqlite:///academe.db'

def init_settings(settings={}):
    settings = dict(settings)
    settings.setdefault('jinja2.directories', 'academe:templates')
    settings.setdefault('academe.db_connect_string',
                        DEFAULT_CONNECT_STRING)

    settings['academe.db_engine'] = sqlalchemy.create_engine(
        settings['academe.db_connect_string'])
    settings['academe.db_session_factory'] = orm.sessionmaker(
        bind=settings['academe.db_engine'],
        extension=ZopeTransactionExtension())

    return settings

def make_pyramid_app(global_config, **kwargs):
    """ This function returns a WSGI application.
    """

    settings = dict(global_config)
    settings.update(kwargs)
    config = Configurator(root_factory=get_root,
                          settings=init_settings(global_config))
    config.add_renderer('.html', renderer_factory)
    config.add_static_view('static', 'academe:static')
    config.scan('academe')

    pyramid_app = config.make_wsgi_app()

    return pyramid_app

def make_app(global_config, **kwargs):
    """ This function returns a WSGI application.
    """

    app = tm.TM(make_pyramid_app(global_config, **kwargs))
    return app
