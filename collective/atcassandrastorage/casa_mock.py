# -*- coding: utf-8 -*-
#
# File: .py
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


COLUMN_FAMILIES = {}
class MockCF(object):
    def __init__(self, db, keyspace, name):
        self.name=name
        self.data = dict()
        self.timestamp = 0

    def get(self, key):
        return self.data[key]

    def insert(self, key, value):
        if key in self.data:
            self.data[key].update(value)
        else:
            self.data[key] = value
        self.timestamp += 1
        return self.timestamp

    def remove(self, key, columns=None):
        if columns is None:
            del self.data[key]
        else:
            for c in columns:
                del self.data[key][c]

    def get_count(self, key):
        if key in self.data:
             return len(self.data[key].keys())
        return 0

    def __contains__(self, key):
        return key in self.data

    def __repr__(self):
        return "<MockCF name=%s>" % self.name

def ColumnFamily(db, keyspace, name):
   cfname = "%s.%s" % (keyspace, name)
   if name in COLUMN_FAMILIES:
       return COLUMN_FAMILIES[cfname]
   else:
       cf = MockCF(db, keyspace, name)
       COLUMN_FAMILIES[cfname] = cf
       return cf

def ZapData():
    for d in COLUMN_FAMILIES.keys():
        del COLUMN_FAMILIES[d]

def mock():
    import pycassa
    pycassa._ColumnFamily = pycassa.ColumnFamily
    pycassa.ColumnFamily = ColumnFamily

    from collective.atcassandrastorage import db
    def get_column_family(keyspace, name):
        return ColumnFamily(None, keyspace, name)
    db._get_column_family = db.get_column_family
    db.get_column_family = get_column_family


def unmock():
    import pycassa
    from collective.atcassandrastorage import db
    pycassa.ColumnFamily = pycassa._ColumnFamily
    db.get_column_family = db._get_column_family

# vim: set ft=python ts=4 sw=4 expandtab :
