=============================
collective.atcassandrastorage
=============================

:Author: Stefan Eletzhofer
:Date: 2010-05-28


Abstract
========

An Archetype field storage which uses a *cassandra* backing store.

Reasoning
=========

For a customer project I'm doing right now I'm using *cassandra* as a storage
backend for *Plone FormGen* data.  Now the need did arise to also have specific
fields of AT content types to be stored in cassandra as well.


Design decisions
================

- configuration of the cassandra clients done by using *plone.app.registry*

- per-field configurable *keyspace* and *column family* for fields

- The **UID** of the instance object is used as a *key* in the specified
  *column family* (remember that an *insert* in cassandra is essentially an
  *update*)

- using *pycassa* as glue library

Usage
=====

Import the storage and attach it to a field in your AT Schema::


    from collective.atcassandrastorage.storage import CassandraFieldStorage

    MySchema = atapi.Schema(
          ...
          StringField("afield",
                  storage=CassandraFieldStorage("AKeyspace", "AColumnFamily"),
                  ),
          ...
    )

This will store and fetch data for *afield* from a cassandra database using
the keyspace *AKeyspace* and the column family *AColumnFamily*.

Configuration
=============

Configuration is done using *plone.app.registry*.  Visit the registry in
Plone's control panel and configure the values, they should be pretty much
obvious.

Dependencies
============

*plone.app.registry*
    for configuration

*pycassa*
    python Cassandra glue library

Links
=====

**cassandra**
    http://cassandra.apache.org/

**archetypes**
    http://plone.org/products/archetypes

**pycassa**
    http://github.com/vomjom/pycassa

..  vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
