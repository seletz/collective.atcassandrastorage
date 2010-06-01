# -*- coding: utf-8 -*-
#
# File: session.py
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


import logging
import pycassa
import threading

from collective.atcassandrastorage import settings
from collective.atcassandrastorage import db

logger = logging.getLogger("collective.atcassandrastorage")


remove_marker = object()


class ColumnFamily(object):
    """A very simple version of a cassandra CF which
       delays writing."""

    def __init__(self, session, name):
        self.session = session
        self.name = name
        self.data = dict()
        self.removed = defaultdict(list) # removed columns per key
        self.column_family = pycassa.ColumnFamily(session.client, session.keyspace, name)

    def __setitem__(self, key, data):
        assert isinstance(data, dict), "Can only set dict types"

        if key in self.data:
            if self.data[key] is remove_marker:
                self.data[key] = data

            if key in self.removed:
                for k in data.keys():
                    self.removed[keys].remove(k)
                if len(self.removed[key]) == 0:
                    del self.removed[key]

            self.data[key].update(data)
        else:
            data = self.column_family.get(key)
            self.data[key] = data

    def __getitem__(self, key):
        if key in self.data:
            if self.data[key] is remove_marker:
                return AttributeError("key %s removed in session." % key)
            return self.data[key]

        # not in session -- delegate
        return self.column_family.get(key)

    def remove(self, key, columns=None):
        if columns:
            self.removed[key] = self.data[key].keys()
            for c in columns:
                if c in self.data[key]:
                    self.removed[key].append(c)
                    del self.data[key][c]

            if len(self.data[key].keys()) == 0:
                self.data[key] = remove_marker
        else:
            self.removed[key] = self.data[key].keys()
            self.data[key] = remove_marker

    def __repr__(self):
        return "<ColumnFamily: %d key changes, %d removes>" % (
                len(self.data.keys()),
                len(self.removed.keys()))


class ThreadLocalCassandraSession(object):
    """A per-keyspace cassandra session"""

    def __init__(self, keyspace):
        self.keyspace = keyspace
        self.client = db.get_client(keyspace)
        self._tl = threading.local()
        self._tl.column_families = dict()

    def in_session(self, name):
        return name in self._tl.column_families

    __contains__ = in_session

    def flush(self):
        pass

    def get_column_family(self, name):
        cf = self._tl.column_families.get(name, None)
        if cf is None:
            return ColumnFamily(self, name)
        return cf

    def __repr__(self):
        return "<ThreadLocalCassandraSession keyspace=%s id=%s>" %(self.keyspace, id(self))


def make_session():
    """Make a new session"""
    tl = threading.local()
    if getattr(tl, "cassandra_sessions", None) is None:
        tl.cassandra_sessions= dict()

    if keyspace in tl.cassandra_sessions:
        return tl.get(keyspace)

    session = ThreadLocalCassandraSession(keyspace)
    tl.cassandra_sessions[keyspace] = session
    logger.info("New session : %s" % (repr(session)))

    return session


# vim: set ft=python ts=4 sw=4 expandtab :
