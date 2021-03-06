import unittest

from pyramid.configuration import Configurator
from pyramid import testing


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def test_my_view(self):
        from academe.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'academe')


""" test models
"""


class AcademicModelTests(unittest.TestCase):

    def _getTargetClass(self):
        from academe.models import Academic
        return Academic

    def _makeOne(self):
        return self._getTargetClass()()

    def test_it(self):
        page = self._makeOne()
        self.assertEqual(page.__parent__, None)
        self.assertEqual(page.__name__, None)


class BlogModelTests(unittest.TestCase):

    def _getTargetClass(self):
        from academe.models import PageMaker
        return PageMaker

    def _makeOne(self):
        return self._getTargetClass()()

    def test_it(self):
        page = self._makeOne()
        self.assertEqual(page.__parent__, None)
        self.assertEqual(page.__name__, None)


class AppmakerTests(unittest.TestCase):

    def _callFUT(self, zodb_root):
        from academe.models import appmaker
        return appmaker(zodb_root)

    def test_w_app_root(self):
        app_root = object()
        root = {'app_root': app_root}
        self._callFUT(root)
        self.failUnless(root['app_root'] is app_root)
