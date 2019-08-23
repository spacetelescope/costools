#! /usr/bin/env python

"""splittag - Split TIME-TAG files into multiple files."""

from __future__ import absolute_import, division, print_function # confidence unknown

__usage__ = """

1. To run this task from within Python::

    >>> import costools
    >>> from stsci.tools import teal
    >>> teal.teal("splittag")

    or:

    >>> import costools
    >>> costools.splittag.splittag("rootname_corrtag_a.fits", "split3s",
            starttime=0., increment=3., endtime=1000.,
            time_list="")

    or:

    >>> from costools import splittag
    >>> splittag.splittag("rootname_corrtag_a.fits", "split250s",
                          starttime=None, increment=None, endtime=None,
                          time_list="0, 250, 500, 750, 1000")

.. note:: make sure the costools package is on your Python path

2. To run this task using the TEAL GUI to set the parameters under PyRAF::

    >>> import costools
    >>> teal splittag                   # or 'epar splittag'
"""

__doc__ += __usage__

from stsci.tools import parseinput, teal

import getopt
from calcos import calcosparam
from calcos import splittag as SPLT
from . import costoolsutil

__taskname__ = "splittag"
__version__ = "1.0"
__vdate__ = "2013 October 10"
__author__ = "Phil Hodge, STScI, October 2013."

def main():
    """Split corrtag files by time."""

    try:
        (options, pargs) = getopt.getopt(args, "hqvr",
                                         ["version",
                                          "help"])
    except Exception(error):
        print(str(error))
        prtOptions()
        return

    help = False
    verbosity = calcosparam.VERBOSE

    # If still "" after reading arguments, "" will be changed to None.
    starttime = ""
    increment = ""
    endtime = ""
    time_list = ""

    for i in range(len(options)): 
        if options[i][0] == "--version":
            print("%s" % __version__)
            return
        if options[i][0] == "-r":
            print("%s (%s)" % (__version__, __vdate__))
            return
        if options[i][0] == "-h":
            help = True
        elif options[i][0] == "--help":
            help = True
        if options[i][0] == "-q":
            verbosity = calcosparam.QUIET
        elif options[i][0] == "-v":
            verbosity = calcosparam.VERY_VERBOSE

    if help:
        print(getHelpAsString())
        # print(__doc__)
        # print(__usage__)
        # print("\t", __version__ + " (" + __vdate__ + ")")
        return

    nargs = len(pargs)
    if nargs < 2 or nargs > 7:
        prtOptions()
        return

    if nargs >= 3:
        starttime = pargs[2]
    if nargs >= 4:
        increment = pargs[3]
    if nargs >= 5:
        endtime = pargs[4]
    if nargs >= 6:
        time_list = pargs[5]
    if nargs == 7:
        verbosity = int(pargs[6])

    if starttime.strip() == "":
        starttime = None
    else:
        starttime = float(starttime)
    if increment.strip() == "":
        increment = None
    else:
        increment = float(increment)
    if endtime.strip() == "":
        endtime = None
    else:
        endtime = float(endtime)

    splittag(infiles=pargs[0], outroot=pargs[1],
             starttime=starttime, increment=increment, endtime=endtime,
             time_list=time_list, verbosity=verbosity)

def prtOptions():
    """Print a list of command-line options and arguments."""

    print("The command-line arguments are:")
    print("  -h (print help)")
    print("  --help (print help)")
    print("  -r (print the full version string)")
    print("  --version (print the version number)")
    print("  -v (very verbose -- print more messages than the default)")
    print("  -q (quiet -- print almost no messages)")
    print("")
    print("Following the options, give the following:")
    print("  Name of input file, optionally including wildcards")
    print("  String with which to begin output file names")
    print("  Time at beginning of first interval, or ''")
    print("  Length (s) of each time interval, or ''")
    print("  Time at end of last interval, or ''")
    print("  Comma- or blank-separated string of times for intervals")
    print("  Verbosity (0 [low], 1 [default], or 2 [high])")

def splittag(infiles, outroot, starttime=None, increment=None, endtime=None,
             time_list=None, verbosity=calcosparam.VERBOSE):

    if not time_list:
        time_list = None

    SPLT.splittag(infiles=infiles, outroot=outroot,
                  starttime=starttime, increment=increment, endtime=endtime,
                  time_list=time_list, verbosity=verbosity)

#
#### Interfaces used by TEAL
#
def run(configobj=None):
    """TEAL interface for running this code."""
    ### version 2013 October 9

    splittag(infiles=configobj["infiles"],
             outroot=configobj["outroot"],
             starttime=configobj["starttime"],
             increment=configobj["increment"],
             endtime=configobj["endtime"],
             time_list=configobj["time_list"],
             verbosity=configobj["verbosity"])

def getHelpAsString(fulldoc=True):
    """Return help info from <module>.help in the script directory"""

    if fulldoc:
        basedoc = __doc__
    else:
        basedoc = ""
    helpString = basedoc + "\n"
    helpString += "Version " + __version__ + "\n"

    helpString += teal.getHelpFileAsString(__taskname__, __file__)

    return helpString

# Set up doc string without the module level docstring included for
# use with Sphinx, since Sphinx will already include module level docstring
# xxx splittag.__doc__ = getHelpAsString(fulldoc=False)

def help():
    print(getHelpAsString())

if __name__ == "__main__":

    main()
