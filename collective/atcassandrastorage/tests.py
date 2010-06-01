import unittest
import doctest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import collective.atcassandrastorage
from collective.atcassandrastorage import casa_mock
from collective.atcassandrastorage import settings


class FunctionalTestCase(ptc.PloneTestCase):


    @property
    def COLUMN_FAMILIES(self):
        return casa_mock.COLUMN_FAMILIES

    def zap_data(self):
        casa_mock.ZapData()

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(collective.atcassandrastorage)
            fiveconfigure.debug_mode = False

            casa_mock.mock()

            settings._get_config = settings.get_config

            def fake_config():
                class FakeConfig(object):
                    servers = ["127.0.0.1:9160"]
                    username = "user"
                    password = "pass"
                    connection_timeout = 42

                return FakeConfig()
            settings.get_config = fake_config



        @classmethod
        def tearDown(cls):
            settings.get_config = settings._get_config
            casa_mock.unmock()

class DocTestCase(unittest.TestCase):

    @property
    def COLUMN_FAMILIES(self):
        return casa_mock.COLUMN_FAMILIES

    def zap_data(self):
        casa_mock.ZapData()

    def setUp(cls):
        casa_mock.mock()

        settings._get_config = settings.get_config

        def fake_config():
            class FakeConfig(object):
                servers = ["127.0.0.1:9160"]
                username = "user"
                password = "pass"
                connection_timeout = 42

            return FakeConfig()
        settings.get_config = fake_config



    def tearDown(cls):
        settings.get_config = settings._get_config
        casa_mock.unmock()


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='collective.atcassandrastorage',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.atcassandrastorage.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
            #'storage.rst', package='collective.atcassandrastorage',
            #test_class=FunctionalTestCase),

        #doctest.DocFileSuite(
        ztc.ZopeDocFileSuite(
            'session.rst', package='collective.atcassandrastorage',
            test_class=DocTestCase),


        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='collective.atcassandrastorage',
        #    test_class=FunctionalTestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
