from academe import make_app, init_settings
from academe import models

import logging

from werkzeug import script, serving


def init_logging(verbosity):
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('academe').setLevel(logging.WARNING)

    if verbosity >= 1:
        logging.getLogger('werkzeug').setLevel(logging.INFO)
        logging.getLogger('academe').setLevel(logging.INFO)
    if verbosity >= 2:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        logging.getLogger('academe').setLevel(logging.DEBUG)
    if verbosity >= 3:
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.INFO)
    if verbosity >= 4:
        logging.getLogger('werkzeug').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)

def main():

    def action_runserver(hostname=('h', '0.0.0.0'), port=('p', 8080),
                         debug=('d', False), verbosity=('v', 0)):
        '''Run the development server.

        :param debug: run in debug mode
        :param verbosity: increase level of logging for more verbose logging
        '''
 
        logging.basicConfig()
        init_logging(verbosity)

        serving.run_simple(hostname, port,
                           make_app({'reload_templates': debug,
                                     'reload_resources': debug}),
                           use_reloader=debug,
                           use_debugger=debug,
                           use_evalex=debug)

    def action_syncdb():
        '''Ensure tables exist in the configured database.
        '''
        settings = init_settings()
        models.Base.metadata.create_all(settings['academe.db_engine'])

    script.run()


if __name__ == '__main__':
    main()
