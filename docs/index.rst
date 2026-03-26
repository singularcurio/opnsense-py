opnsense-py
===========

A synchronous Python client library and CLI for the `OPNsense <https://opnsense.org>`_ REST API.

**Features:**

- Full coverage of the OPNsense REST API across 26+ core modules and plugins
- Typed Pydantic models for all request and response objects
- Automatic pagination via ``search_all`` helpers
- Typed exception hierarchy for clean error handling
- ``opn`` / ``opnsense`` CLI with table, JSON, and plain output formats
- Three-tier configuration: config file → environment variables → CLI flags

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   cli
   library

.. toctree::
   :maxdepth: 2
   :caption: Module Reference

   modules_overview
   api/modules

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
