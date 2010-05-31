import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import collective.atcassandrastorage
from collective.atcassandrastorage import casa_mock


class TestCase(ptc.PloneTestCase):

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


        @classmethod
        def tearDown(cls):
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
        ztc.ZopeDocFileSuite(
            'storage.rst', package='collective.atcassandrastorage',
            test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='collective.atcassandrastorage',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
