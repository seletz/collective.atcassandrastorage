=======================================
collective.atcassandrastorage: Sessions
=======================================

Abstract
========

Cassandra sessions to be used with a zope transaction manager.

Session Object
==============

The session object is a *thread local*, per *keyspace* session which
essentially deleys *writes* to *column families*.  Writes are then
eventuelly done if the zope transaction is committed.

The session object lives in the *session* module::

    >>> from collective.atcassandrastorage import session

There's a factory function for new sessions.  This will return a session
which is unique per thread, and needs to be called with an *keyspace*
argument::

    >>> session.make_session("Archetypes")
    <ThreadLocalCassandraSession keyspace=Archetypes id=...>

    >>> sess  = session.make_session("Archetypes")
    >>> sess2 = session.make_session("Archetypes")
    >>> sess == sess2
    True

The session object itself has a mapping interface::

    >>> sess["Foo"]
    <ColumnFamily Foo: 0 key changes, 0 removes>
    >>> len(sess)
    1
    >>> "Foo" in sess
    True
    >>> _ = sess["Bar"]
    >>> [cf.name for cf in sess]
    ['Foo', 'Bar']

Column Families
===============

To do something, we need a Column Family::

    >>> cf = sess.get_column_family("ExampleType")
    >>> cf
    <ColumnFamily ExampleType: 0 key changes, 0 removes>


reading
-------

Reads fetch directly from cassandra::

    >>> cf["somekey"]
    Traceback (most recent call last):
    ...
    KeyError: 'somekey'

Prep some data into our mock cassandra::

    >>> _ =self.COLUMN_FAMILIES["Archetypes.ExampleType"].insert("somekey",
    ...    {"column1": "value1", "column2": "value2"})

... dan do it again::

    >>> cf["somekey"]
    {'column1': 'value1', 'column2': 'value2'}

inserts
-------

Inserts are delayed::

    >>> cf.insert("anotherkey", {"column": "value"})
    >>> "anotherkey" in self.COLUMN_FAMILIES["Archetypes.ExampleType"]
    False
    >>> "anotherkey" in cf.data
    True

Writes are "committed" if the session is flushed::

    >>> sess.flush()
    >>> "anotherkey" in self.COLUMN_FAMILIES["Archetypes.ExampleType"]
    True
    >>> "anotherkey" in cf.data
    False

removes
-------

Removes are delayed, too.  Let's remove a row::

    >>> cf.remove("anotherkey")

The row is still in the database, nothing changed yet::

    >>> "anotherkey" in self.COLUMN_FAMILIES["Archetypes.ExampleType"]
    True

But it's no longer there if we use our cf::

    >>> cf["anotherkey"]
    AttributeError('key anotherkey removed in session.',)

But we know that it has been removed::

    >>> "anotherkey" in cf.removed
    True

And we know the colums that were removed::

    >>> cf.removed["anotherkey"]
    ['column']

Flush the session and it will be reflected in the database::

    >>> sess.flush()
    >>> "anotherkey" in self.COLUMN_FAMILIES["Archetypes.ExampleType"]
    False

And we no longer keep track of it::

    >>> "anotherkey" in cf.removed
    False

Cassandra supports partial removal of row columns, too.  We support this
also.  Let's remove "comumn 1" from "somekey"::

    >>> cf.remove("somekey", columns=["column1",])

We still see the other column::

    >>> cf["somekey"]
    {'column2': 'value2'}

We keep track of that key and the removed column::

    >>> "somekey" in cf.removed
    True
    >>> cf.removed["somekey"]
    ['column1']



..  vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
