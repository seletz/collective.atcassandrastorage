# -*- coding: utf-8 -*-
#
# File: db.py
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
__revision__  = "$Revision: 5003 $"
__version__   = '$Revision: 5003 $'[11:-2]

import os
import sys

import logging

import pycassa
import urlparse

from collective.atcassandrastorage import settings

logger = logging.getLogger("collective.pfg.cassandra")

def get_client(keyspace):
    config = settings.get_config()

    logger.info("get_client: servers: %s, timeout: %s, user: %s, pass: %s" % (
        config.servers,
        config.connection_timeout,
        config.username,
        config.password))

    client = pycassa.connect_thread_local(
                config.servers,
                timeout=config.connection_timeout
            )

    cred = dict(username=config.username, password=config.password)
    client.login(keyspace, cred)
    logger.info("get_client => %s" % repr(client))
    return client

def get_column_family(keyspace, name):
    client = get_client(keyspace)
    return pycassa.ColumnFamily(client, keyspace, name)

# vim: set ft=python ts=4 sw=4 expandtab :

