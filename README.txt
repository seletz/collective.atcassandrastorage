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
backend for *Plone FormGen** data.  Now the need did arise to also have specific
fields of AT content types to be stored in cassandra as well.


Design decisions
================

- configuration of the cassandra clients done by using *plone.app.registry*

- per-field configurable *keyspace* and *column family* for fields

- The **UID** of the instance object is used as a *key* in the specified
  *column family* (remember that an *insert* in cassandra is essentially an
  *update*)

- using *pycassa* as glue library


Links
=====

**cassandra**
    http://cassandra.apache.org/

**archetype**
    http://plone.org/products/archetypes

..  vim: set ft=rst tw=75 nocin nosi ai sw=4 ts=4 expandtab:
