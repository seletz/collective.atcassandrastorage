# -*- coding: utf-8 -*-
#
# File: tx.py
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

from zope import interface
from zope import component

import transaction
from transactions.interfaces import IDataManager

from Products.Archetypes.Field import IField

from collective.atcassandrastorage.interfaces import ITransactionAware

# this is mostly taken from collective.lead with inspirations from
# zope.sqlalchemy and ore.sqlalchemy.  Thanks, guys!

class ThreadLocalCassandraTransaction(object):

    interface.implements(ITransactionAware)
    component.adapts(IField)

    def __init__(self, context):
        self.context = context # the AT Field

    def begin(self):
        assert not self.active, "Xaction already active."
        transaction.get().join(ThreadlocalCassandraDataManager(self))

    @property
    def active(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

class ThreadlocalCassandraDataManager(object):
    """Instances of this class will be used to 'join' Zope's transactions."""
    implements(IDataManager)

    def __init__(self, tx):
        self.tx = tx # these are ThreadLocalCassandraTransaction instances

    def abort(self, trans):
        # sometimes tx is None
        if self.tx is not None:
            self.tx.rollback()
            self.tx = None
        
    def commit(self, trans):
        pass

    def tpc_begin(self, trans):
        pass

    def tpc_vote(self, trans):
        self.tx.commit()
        self.tx = None

    def tpc_finish(self, trans):
        pass

    def tpc_abort(self, trans):
        self.abort(trans)

    def sortKey(self):
        # Try to sort last, so that we vote last - we commit in tpc_vote(),
        # which allows Zope to roll back its transaction if Cassandra throws a
        # error
        return "~catcasst:%d" % id(self.tx)

# vim: set ft=python ts=4 sw=4 expandtab :
