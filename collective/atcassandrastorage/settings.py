# -*- coding: utf-8 -*-
#
# File: settings.py
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

from zope.component import adapter
from zope.component import getUtility

from plone.registry.interfaces import IRegistry
from plone.registry.interfaces import IRecordModifiedEvent

from collective.atcassandrastorage.interfaces import ICassandraSettings


log = logging.getLogger("collective.atcassandrastorage")


@adapter(ICassandraSettings, IRecordModifiedEvent)
def settings_changed(settings, event):
    log.warning("Cassandra database settings changed")
    # XXX: update connections?


def get_config():
    registry = getUtility(IRegistry)
    return registry.forInterface(ICassandraSettings)

# vim: set ft=python ts=4 sw=4 expandtab : 
