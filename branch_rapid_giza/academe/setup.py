import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

required = ['pyramid >= 1.0a3',
            'pyramid_jinja2',
            'Jinja2 > 2.5.1',
            'SQLAlchemy >= 0.6.1',
            'zope.sqlalchemy >= 0.6',
            'repoze.tm2 >= 1.0a5',
            'Werkzeug >= 0.6.1']

setup(name='academe',
      version='0.1',
      description='academe - a web application',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=required,
      tests_require=required,
      test_suite="academe",
      entry_points = """\
      [console_scripts]
      academe=academe.main:main
      [paste.app_factory]
      pyramid-app=academe:make_pyramid_app
      app=academe:make_app
      """
      )
