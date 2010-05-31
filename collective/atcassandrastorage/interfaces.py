
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


from zope import interface
from zope import schema

class ICassandraSettings(interface.Interface):

    connection_timeout = schema.Int(title=u"The connection timeout in seconds to use", default=5)
    servers = schema.List(
            title=u"Cassandra Servers",
            unique=True,
            value_type=schema.TextLine(title=u"Server entry")
            )

    username = schema.TextLine(title=u"The cassandra username")
    password = schema.TextLine(title=u"The cassandra password")

class IInstanceKey(interface.Interface):
    """An adapter which calculates the cassandra column family key for a given
       instance"""

    def key():
       """Calculate and return the key to be used for the context"""

# vim: set ft=python ts=4 sw=4 expandtab :
