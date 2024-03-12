from __future__ import absolute_import, division         # confidence high

from importlib.metadata import version

__version__ = version(__name__)

from . import timefilter
from . import splittag
from . import x1dcorr

# These lines allow TEAL to print out the names of TEAL-enabled tasks
# upon importing this package.
import os
from stsci.tools import teal

teal.print_tasknames(__name__, os.path.dirname(__file__))
