#! /usr/bin/env python

# Add the S_REGION keyword to raw files
#
import glob
import argparse

from calcos import cosutil
from astropy.io import fits

__version__ = '0.1'
def main(dry_run=False):
    """Add the S-region keyword to all COS FITS files in the current
    directory that meet the following criteria:

    Filename ends with one of ['rawtag.fits',
                               'rawtag_a.fits',
                               'rawtag_b.fits',
                               'rawaccum.fits',
                               'rawaccum_a.fits',
                               'rawaccum_b.fits',
                               'rawacq.fits']

    The S_REGION keyword will have the value
    'CIRCLE ra_aper dec_aper diameter'
    where ra_aper and dec_aper are in decimal degrees and are read from
    the extension 1 header, and diameter = 2.5/3600.0, which is the diameter
    of the PSA and BOA in decimal degrees.

    The keyword will be added after the PA_APER keyword in the extension 1
    header

    """
    endings = ['rawtag.fits',
               'rawtag_a.fits',
               'rawtag_b.fits',
               'rawaccum.fits',
               'rawaccum_a.fits',
               'rawaccum_b.fits',
               'rawacq.fits']

    fitsfiles = glob.glob('*.fits')
    for file in fitsfiles:
        for ending in endings:
            if file.endswith(ending):
                add_s_region(file, dry_run)
    return

def add_s_region(file, dry_run):

    open_mode = 'readonly'
    if not dry_run: open_mode = 'update'

    with fits.open(file, mode=open_mode) as f1:
        if (len(f1) < 2):
            cosutil.printWarning("File {} has only {} extensions".format(file, len(f1)))
            cosutil.printContinuation("Need at least 2")
            return
        prihdr = f1[0].header
        if prihdr['INSTRUME'] != 'COS':
            cosutil.printWarning("File {}: Instrument is not COS".format(file))
            return

        ext1hdr = f1[1].header
        try:
            ra_aper = ext1hdr['RA_APER']
            dec_aper = ext1hdr['DEC_APER']
            pa_aper = ext1hdr['PA_APER']
        except KeyError:
            cosutil.printWarning('One or more of RA_APER, DEC_APER, PA_APER is not present')
            cosutil.printContinuation('in extension 1 header of file {}'.format(file))
            return
        diameter = 2.5 / 3600.0
        s_region = 'CIRCLE {0:.8f} {1:.7f} {2:.8f}'.format(ra_aper, dec_aper, diameter)
        if not dry_run:
            try:
                existing_s_region = ext1hdr['S_REGION']
                ext1hdr['S_REGION'] = (s_region, 'Spatial extent of the observation')
                cosutil.printMsg("Using existing S_REGION keyword in file {}".format(file))
            except KeyError:
                ext1hdr.insert('PA_APER', ('S_REGION', s_region, 'S_region string'), after=True)
                cosutil.printMsg('Added S_REGION keyword to {}'.format(file))
            cosutil.printMsg("Setting value to '{}'".format(s_region))
        else:
            cosutil.printMsg("File {} has S_REGION = '{}'".format(file, s_region))
            cosutil.printMsg("Dry-run - no changes made to science header")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
    """Add S_REGION value to raw data headers"""
    )

    parser.add_argument(
        '--dry_run', action='store_true',
        help="Calculate S_REGION value, but don't write to data header[s]")

    parser.add_argument('-v', '--version', help='Print version info', action='version',
    version = __version__)

    args = parser.parse_args()

    if '--version' in args:
        print(__version__)
        sys.exit(0)

    main(dry_run=args.dry_run)
