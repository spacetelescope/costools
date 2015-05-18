# split string on commas and/or spaces --> list
# remove duplicates and "effective duplicates" (which means
#     xyz_a.fits == xyz_b.fits == xyz.fits)
# expand environment variables
# create output directory if it doesn't already exist

from __future__ import print_function
import glob
import os

MAX_COUNT = 100

#    if outdir:
#        outdir = os.path.expandvars(outdir)
#    createOutputDirectory(outdir)

def expandFilename(filename):
    """Get the actual file name.

    Parameters
    ----------
    filename: str
        A file or directory name.

    Returns
    -------
    full_file_name: str
        The real directory name.
    """

    fname = filename
    done = False
    count = 0
    while not done:
        temp = os.path.expandvars(fname)        # $stuff/dir
        count += 1
        if temp == fname:
            done = True
        fname = temp
        if count >= MAX_COUNT:
            break
    if not done:
        print("%d iterations exceeded while expanding " \
              "variables for file name %s" % (MAX_COUNT, filename))
    fname = os.path.abspath(fname)              # ../dir
    fname = os.path.expanduser(fname)           # ~/dir
    full_file_name = os.path.normpath(fname)    # remove redundant strings

    return full_file_name

def createOutputDirectory(outdir):
    """Check whether outdir exists, and create it if necessary.

    If outdir was specified but doesn't exist, create it.

    Parameters
    ----------
    outdir: str or None
        Name of output directory.
    """

    if outdir:
        full_outdir = expandFilename(outdir)
        if os.path.lexists(full_outdir):
            if not os.path.isdir(full_outdir):
                raise RuntimeError("'%s' is a file; should be a directory." %
                                   outdir)
        else:
            print("Creating output directory '%s'." % outdir)
            os.mkdir(full_outdir)

def splitInputString(input):
    """Split on comma and/or space.

    Parameters
    ----------
    input: str
        One or more values (e.g. file names), separated by a comma and/or
        a space.

    Returns
    -------
    words: list of strings
    """

    if isinstance(input, str):
        if input.strip() == "":
            words = [""]
        else:
            # First split on comma, then check for blanks.
            temp_words = input.split(",")
            words = []
            for word in temp_words:
                word = word.strip()
                if word == "":
                    words.append("")
                else:
                    words.extend(word.split())
    else:
        words = input

    return words

def uniqueInput(infiles, unique=False):
    """Remove effective duplicates from the list of files.

    This function also expands environment variables and wildcards.
    Aside from that, the order of the input file names will be preserved.

    Parameters
    ----------
    infiles: list of strings
        List of input file names.

    unique: bool
        If unique is True, drop duplicates and effective duplicates
        from the list of file names.  "Effective duplicate" means that
        the root names are the same, but the segment might differ.

    Returns
    -------
    unique_files: list of strings
        The list of input files but with duplicates removed.
    """

    # expand environment variables and wildcards
    allfiles = []
    for file in infiles:
        template = expandFilename(file)
        files = glob.glob(template)
        files.sort()
        allfiles.extend(files)

    if len(allfiles) <= 1:
        return allfiles

    if not unique:
        return allfiles

    inlist = copy.copy(allfiles)
    inlist.sort()

    newlist = [inlist[0]]
    for i in range(1, len(inlist)):
        n = len(inlist[i])
        if inlist[i].endswith("_a.fits"):
            n -= 7
        elif inlist[i].endswith("_b.fits"):
            n -= 7
        elif inlist[i].endswith(".fits"):
            n -= 5
        if inlist[i][:n] != inlist[i-1][:n]:
            newlist.append(inlist[i])

    unique_files = []
    for input in allfiles:
        if input in newlist and \
           input not in unique_files:
            unique_files.append(input)

    return unique_files
