#! /usr/bin/env python

"""x1dcorr - Extract 1-D spectra."""

from __future__ import absolute_import, division, print_function # confidence high

__usage__ = """

1. To run this task from within Python::

    >>> from costools import x1dcorr
    >>> x1dcorr.x1dcorr(["rootname_corrtag_a.fits",
                         "rootname_corrtag_b.fits"], outdir="out/",
                        update_input=True,
                        find=True, cutoff=5., verbosity=2)

    >>> x1dcorr.x1dcorr(["rootname_corrtag_a.fits"], outdir="out/",
                        update_input=True,
                        find=False,
                        location=527.88, extrsize=15,
                        verbosity=2)
    >>> x1dcorr.x1dcorr(["rootname_corrtag_b.fits"], outdir="out/",
                        update_input=True,
                        find=False,
                        location=586.68, extrsize=15,
                        verbosity=2)

    >>> x1dcorr.x1dcorr(["rootname_corrtag.fits"], outdir="out/",
                        find=False,
                        location=[196.84, 290.87, 424.62],
                        extrsize=[15, 15, 15])


.. note:: make sure the costools package is on your Python path

2. To run this task using the TEAL GUI to set the parameters under PyRAF::

    >>> import costools
    >>> teal x1dcorr                    # or 'epar x1dcorr'

3. To run this task from the operating system command line::

    # Extract a 1-D spectrum xxx
"""

__doc__ += __usage__

import copy
import getopt
import glob
import numpy as np
from stsci.tools import parseinput, teal
from calcos import x1d as X1D
from calcos import calcosparam
from . import costoolsutil

__taskname__ = "x1dcorr"
__version__ = "1.0"
__vdate__ = "2013 October 9"
__author__ = "Phil Hodge, STScI, October 2013."

def main():
    """Run the CalCOS 1-D extraction function."""

    try:
        (options, pargs) = getopt.getopt(args, "hqvro:",
                                         ["version",
                                          "help",
                                          "find="])
    except Exception as error:
        print(str(error))
        prtOptions()
        return

    help = False
    verbosity = calcosparam.VERBOSE
    outdir = None

    # Parameters for finding the target in XD.
    find = False
    cutoff = None

    location = ""
    extrsize = ""

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
        elif options[i][0] == "-o":
            outdir = options[i][1]
        elif options[i][0] == "--find":
            temp = options[i][1].lower()
            if temp == "yes" or temp == "true":
                find = True
            elif temp == "no" or temp == "false":
                find = False
            else:
                try:
                    cutoff = float(temp)
                except ValueError:
                    prtOptions()
                    cosutil.printError("Don't understand '--find %s'" %
                                       options[i][1])
                    return
                if cutoff < 0.:
                    prtOptions()
                    cosutil.printError("Cutoff for --find cannot be negative.")
                    return
                find = True

    if help:
        print(getHelpAsString())
        # print(__doc__)
        # print(__usage__)
        # print("\t", __version__ + " (" + __vdate__ + ")")
        return

    nargs = len(pargs)
    if nargs < 1:
        prtOptions()
        return

    x1dcorr(pargs, outdir, update_input,
            find=find, cutoff=cutoff,
            location=location, extrsize=extrsize,
            verbosity=verbosity)

def prtOptions():
    """Print a list of command-line options and arguments."""

    print("The command-line arguments are:")
    print("  -h (print help)")
    print("  --help (print help)")
    print("  -r (print the full version string)")
    print("  --version (print the version number)")
    print("  -o outdir (output directory name)")
    print("  -v (very verbose -- print more messages than the default)")
    print("  -q (quiet -- print almost no messages)")
    print("  --find yes|no|cutoff (find Y location of spectrum)")
    print("")
    print("Following the options, list one or more corrtag file names")
    print("or raw file names.")

def x1dcorr(input, outdir="", update_input=False,
            find=False, cutoff=None,
            location="", extrsize="",
            verbosity=1):

    # Split the input string into words, expand environment variables and
    # wildcards.
    words = costoolsutil.splitInputString(input)
    infiles = costoolsutil.uniqueInput(words, unique=False)

    if location:
        temp = costoolsutil.splitInputString(location)
        locn = []
        for value in temp:
            locn.append(float(value))
    else:
        locn = None
    if extrsize:
        temp = costoolsutil.splitInputString(extrsize)
        extrsz = []
        for value in temp:
            extrsz.append(float(value))
    else:
        extrsz = None

    X1D.extractSpec(infiles, outdir=outdir,
                    update_input=update_input,
                    location=locn, extrsize=extrsz,
                    find_target={"flag": find, "cutoff": cutoff},
                    verbosity=verbosity)


#
#### Interfaces used by TEAL
#
def run(configobj=None):
    """TEAL interface for running this code."""
    ### version 2013 October 4

    x1dcorr(input=configobj["input"],
            outdir=configobj["outdir"],
            update_input=configobj["update_input"],
            find=configobj["find"],
            cutoff=configobj["cutoff"],
            location=configobj["location"],
            extrsize=configobj["extrsize"],
            verbosity=int(configobj["verbosity"]))

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
# xxx x1dcorr.__doc__ = getHelpAsString(fulldoc=False)

def help():
    print(getHelpAsString())

if __name__ == "__main__":

    main()
