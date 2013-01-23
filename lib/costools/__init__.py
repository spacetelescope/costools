from __future__ import division         # confidence high

if False :
    __version__ = ''
    __svn_version__ = 'Unable to determine SVN revision'
    __full_svn_info__ = ''
    __setup_datetime__ = None

    try:
        __version__ = __import__('pkg_resources').\
                            get_distribution('costools').version
    except:
        pass

else :
    __version__ = '1.1'

try:
    from costools.svninfo import(__svn_version__, __full_svn_info__,
                                 __setup_datetime__)
except ImportError:
    pass

import timefilter

# These lines allow TEAL to print out the names of TEAL-enabled tasks
# upon importing this package.
import os
from stsci.tools import teal
teal.print_tasknames(__name__, os.path.dirname(__file__))
