=======================================
collective.atcassandrastorage: Storage
=======================================

:Author:    $Author: seletz $
:Date:      $Date: 2010-05-28 11:28:32 +0200 (Fr, 28 Mai 2010) $
:Revision:  $Revision: 5054 $

Abstract
========

A doctest for the **collective.atcassandrastorage** AT fileld storage.


Introduction
============

The field storage gets and fetches data from/to cassandra.  This is done by
specifying an instance of the **CassandraFieldStorage** class as the 'storage'
attribute of an AT schema field::

    >>> from collective.atcassandrastorage.storage import CassandraFieldStorage

On construction, the instance of the field storage needs to be initialized with
ihe *keyspace* and the *comumn family* to store and fetch data from::

    >>> storage = CassandraFieldStorage("AT", "ExampleType")
    >>> storage.column_family == "ExampleType"
    True
    >>> storage.keyspace == "AT"
    True

Storage Tests
=============

Ok, now finally test the storage.  We'll get a new instance of the storage
class here, just that the test makes more sense::

    >>> storage = CassandraFieldStorage("AT", "ExampleType")


Now lets's use this storage::

    >>> self.folder.Schema().get("title").storage = storage

And now let's set the Title::

    >>> self.folder.setTitle("Some Title")
    >>> self.folder.Title()
    'Some Title'

Now let's look at the mock cassandra DB and check for the value.  The *key*
used is the *UID* of the instance::

    >>> key = self.folder.UID()

Our mock cassandra does'nt do keyspaces really but uses the keyspace
as a prefix to the column family::

    >>> cf_name = "AT.ExampleType"

Get the data::

    >>> self.COLUMN_FAMILIES[cf_name].get(key)
    {'title': 'Some Title'}


Instance Key Adapters
=====================

The storage uses the *UID* of the instance as a key for cassandra in the
given column family::

    >>> storage.key_for_instance(self.folder) == self.folder.UID()
    True

To be able to alter this behavior, we need to register an adapter from the
instance to the IInstanceKey interface::

    >>> from collective.atcassandrastorage.interfaces import IInstanceKey

So let's test this.  Let's define a fake adapter::

    >>> class MockInstanceKey(object):
    ...     def __init__(self, context):
    ...         pass
    ...
    ...     def key(self):  return "SomeKey"

Now let's register this::

    >>> from zope import component
    >>> from zope import interface
    >>> gsm = component.getGlobalSiteManager()
    >>> gsm.registerAdapter(MockInstanceKey, required=(interface.Interface,), provided=IInstanceKey)

Now let's set the title again, and we should see the storage using a
different key::

    >>> self.folder.setTitle("Just another Title")
    >>> self.COLUMN_FAMILIES["AT.ExampleType"].get("SomeKey")
    {'title': 'Just another Title'}


just clean up the adapter registration::

    >>> gsm.unregisterAdapter(MockInstanceKey, required=(interface.Interface,), provided=IInstanceKey)
    True

..  vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:

