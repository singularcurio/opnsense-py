Installation
============

Requirements
------------

- Python 3.12 or newer
- An OPNsense firewall with API access enabled (*System → Access → Users → API keys*)

Install from PyPI
-----------------

.. code-block:: bash

   # Library only
   pip install opnsense-py

   # Library + CLI (opn / opnsense commands)
   pip install opnsense-py[cli]

Verify the install
------------------

.. code-block:: bash

   python -c "import opnsense_py; print(opnsense_py.__version__)"

   # CLI (requires [cli] extras)
   opn --version

Development install
-------------------

.. code-block:: bash

   git clone https://github.com/yourusername/opnsense-py
   cd opnsense-py
   poetry install --extras cli

See :doc:`contributing` for more on the development workflow.
