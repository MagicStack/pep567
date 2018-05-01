.. image:: https://travis-ci.org/MagicStack/contextvars.svg?branch=master
    :target: https://travis-ci.org/MagicStack/contextvars


PEP 567 Backport
================

This package implements a backport of Python 3.7 ``contextvars``
module (see PEP 567) for Python 3.6 and 3.5.

In Python 3.7, ``contextvars`` uses an immutable mapping type based
on HAMT, which is backported to Python 3.6 and 3.5 as `immutables
<https://github.com/MagicStack/immutables/>`_, and listed as an
optional dependency here as ``HAMT``. It is boosted by C code in
CPython like CPython 3.7, thus recommended for general use.

**Important:** at this moment this package does not provide an
asyncio event loop with PEP 567 support yet.  Stay tuned for updates.


Original "contextvars" Package
==============================

This package replaces the old "contextvars" PyPI package which
repository is available `here <https://github.com/gawen/contextvars>`_.


Documentation
=============

Read the official ``contextvars`` module documentation here:
https://docs.python.org/3.7/library/contextvars.html


`PEP 567 <https://www.python.org/dev/peps/pep-0567/>`_ also provides
a comprehensive overview of the API and explains all design choices.


Installation
============

.. code-block:: bash

    $ pip install contextvars[HAMT]


Usage
=====

.. code-block:: python

    import contextvars

    my_var = contextvars.ContextVar('my_var')

    # ...


Listing as a Dependency
=======================

The good news is that the standard library always takes the
precedence over site packages, so even if a local ``contextvars``
module is installed, the one from the standard library will be used.
Therefore you can simply list ``contextvars[HAMT]`` in your
``requirements.txt`` or ``setup.py`` files.

Another option is to use `"platform specific dependencies"
<http://setuptools.readthedocs.io/en/latest/setuptools.html\
#declaring-platform-specific-dependencies>`_ setuptools feature:

.. code-block:: python

    import setuptools

    setuptools.setup(
        name="Project",
        ...
        install_requires=[
            'contextvars[HAMT];python_version<"3.7"'
        ]
    )


License
=======

Apache 2.0.
