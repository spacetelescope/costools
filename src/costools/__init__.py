from __future__ import absolute_import, division         # confidence high

import importlib.metadata
try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = 'UNKNOWN'


from . import timefilter
from . import splittag
from . import x1dcorr

# These lines allow TEAL to print out the names of TEAL-enabled tasks
# upon importing this package.
import os
from stsci.tools import teal
teal.print_tasknames(__name__, os.path.dirname(__file__))
