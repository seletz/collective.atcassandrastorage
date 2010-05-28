# -*- coding: utf-8 -*-
#
# File: storage.py
#
# Copyright (c) InQuant GmbH
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__author__    = """Stefan Eletzhofer <stefan.eletzhofer@inquant.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import os
import logging

import pycassa

from zope import interface

from AccessControl import ClassSecurityInfo

from Products.Archetypes.interfaces.storage import IStorage
from Products.Archetypes.Storage import Storage

from Products.Archetypes.Registry import setSecurity
from Products.Archetypes.Registry import registerStorage

from CMFPlone.utils import safe_unicode

from collective.atcassandrastorage import db


logger = logging.getLogger("collective.atcassandrastorage")


class CassandraFieldStorage(Storage):
    """Stores data to a cassandra backing store
    """
    interface.implements(IStorage)

    security = ClassSecurityInfo()

    encoding = "utf-8"

    def __init__(self, keyspace, column_family):
        logger.info("CassandraFieldStorage.__init__: keyspace=%s, column_family=%s" % (keyspace, column_family))
        self.keyspace = keyspace
        self.cf_name = column_family
        self.data = db.get_column_family(keyspace, column_family)

    def key_for_istance(self, instance):
        return instance.getUID()

    security.declarePrivate('get')
    def get(self, name, instance, **kwargs):
        logger.info("CassandraFieldStorage.get: name=%s, instance=%s, kw=%s" % (name, repr(instance), kw))
        key = self.key_for_istance(instance)

        try:
            data = self.data.get(key)
        except (pycassa.NotFoundException, pycassa.NoServerAvailable), e:
            raise AttributeError("CassandraFieldStorage: exception %s accessing %s.%s.%s" %
                    (repr(e), self.keyspace, self.cf_name, key))

        return safe_unicode(data[name], CassandraFieldStorage.encoding)

    security.declarePrivate('set')
    def set(self, name, instance, value, **kwargs):
        logger.info("CassandraFieldStorage.get: name=%s, instance=%s, value=%s ..., kw=%s" % (name, repr(instance), str(value)[:20], kw))
        key = self.key_for_istance(instance)
        self.data.insert(key, {name: value.encode(CassandraFieldStorage.encoding)})

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        logger.info("CassandraFieldStorage.unset: name=%s, instance=%s, kw=%s" % (name, repr(instance), kw))

        key = self.key_for_istance(instance)
        try:
            self.data.remove(key, columns=[name])
        except (pycassa.NotFoundException, pycassa.NoServerAvailable), e:
            pass


setSecurity(CassandraFieldStorage)
registerStorage(CassandraFieldStorage)

# vim: set ft=python ts=4 sw=4 expandtab :
