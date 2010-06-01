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

from collections import defaultdict

from collective.atcassandrastorage import db

logger = logging.getLogger("collective.atcassandrastorage")


remove_marker = object()


class ColumnFamily(object):
    """A very simple version of a cassandra CF which
       delays writing."""

    def __init__(self, session, name):
        self.session = session
        self.name = name
        self.column_family = pycassa.ColumnFamily(session.client, session.keyspace, name)
        self.clear()

    def clear(self):
        self.data = dict()
        self.removed = defaultdict(list) # removed columns per key

    def flush(self):
        for key, row in self.data.iteritems():
            if row is not remove_marker:
                self.column_family.insert(key, row)

        for key, columns in self.removed.iteritems():
            self.column_family.remove(key, columns=columns)

        self.clear()

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
            d = {}
            if self.column_family.get_count(key):
                d = self.column_family.get(key)

            d.update(data)
            self.data[key] = d

    def __getitem__(self, key):
        if key in self.data:
            if self.data[key] is remove_marker:
                return AttributeError("key %s removed in session." % key)
            return self.data[key]

        # not in session -- delegate
        return self.column_family.get(key)

    def insert(self, key, data):
        self[key] = data

    def get(self, key):
        return self[key]

    def remove(self, key, columns=None):
        if columns:
            data = self.get(key)
            dirty = False
            for c in columns:
                if c in data.keys():
                    dirty = True
                    self.removed[key].append(c)
                    del data[c]

            if dirty:
                if len(data.keys()):
                    self.data[key] = data
                else:
                    self.data[key] = remove_marker
        else:
            dirty = False
            if key in self.data:
                removed = self.data[key]
            else:
                removed = self.get(key)

            self.removed[key] = removed.keys()

            self.data[key] = remove_marker

    def __repr__(self):
        return "<ColumnFamily %s: %d key changes, %d removes>" % (
                self.name,
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

    def __getitem__(self, name):
        return self.get_column_family(name)

    def __len__(self):
        return len(self._tl.column_families.keys())

    def __iter__(self):
        for name, cf in self._tl.column_families.iteritems():
            yield cf

    def flush(self):
        for cf in self:
            cf.flush()

    def clear(self):
        for cf in self:
            cf.clear()

    def get_column_family(self, name):
        cf = self._tl.column_families.get(name, None)
        if cf is None:
            cf = ColumnFamily(self, name)
            self._tl.column_families[name] = cf
        return cf

    def __repr__(self):
        return "<ThreadLocalCassandraSession keyspace=%s id=%s>" %(self.keyspace, id(self))

SESSIONS = None

def make_session(keyspace):
    """Make a new session"""
    global SESSIONS
    if not SESSIONS:
        SESSIONS = threading.local()
        SESSIONS.sessions = dict()

    if keyspace in SESSIONS.sessions:
        return SESSIONS.sessions.get(keyspace)

    session = ThreadLocalCassandraSession(keyspace)
    SESSIONS.sessions[keyspace] = session
    logger.info("New session : %s" % (repr(session)))

    return session


# vim: set ft=python ts=4 sw=4 expandtab :
