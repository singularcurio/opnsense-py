import builtins
import sys
import typing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Pydantic v2 evaluates its internal 'Dict[str, Any]' extras annotation using
# eval() in the namespace of each model's defining module.  Models that don't
# explicitly import Dict/Any/List will raise NameError under Sphinx's autodoc
# dynamic importer.  Injecting these names into builtins makes them available
# in every module's globals without modifying source files.
# Pre-import all package modules so they are already in sys.modules when
# Sphinx's autodoc dynamic importer runs.  Without this, the importer loads
# modules in a special isolated environment that breaks Pydantic v2's
# evaluation of forward references (e.g. Dict[str, Any] in extra="allow"
# models whose defining module doesn't import Dict).
import opnsense_py  # noqa: F401
import opnsense_py.modules.core  # noqa: F401
import opnsense_py.modules.plugins  # noqa: F401
import opnsense_py.models  # noqa: F401

project = "opnsense-py"
author = "Justin Refi"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_theme = "sphinx_rtd_theme"
autodoc_member_order = "bysource"
