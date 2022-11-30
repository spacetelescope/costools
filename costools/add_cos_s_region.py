#! /usr/bin/env python

# Add the S_REGION keyword to raw files
#
import glob
import argparse

from calcos import cosutil
from astropy.io import fits

def main(rootnames, dry_run=False):
    """Add the S-region keyword to COS FITS files in the current
    directory that meet the following criteria:

    ['rootname_rawtag.fits',
     'rootname_rawtag_a.fits',
     'rootname_rawtag_b.fits',
     'rootname_rawaccum.fits',
     'rootname_rawaccum_a.fits',
     'rootname_rawaccum_b.fits',
     'rootname_rawacq.fits']

    The S_REGION keyword will have the value
    'CIRCLE ICRS ra_aper dec_aper diameter'
    where ra_aper and dec_aper are in decimal degrees and are read from
    the extension 1 header, and diameter = 2.5/3600.0, which is the diameter
    of the PSA and BOA in decimal degrees.

    The keyword will be added after the PA_APER keyword in the extension 1
    header

    """
    if rootnames is None:
        cosutil.printError("No rootnames specified")
        return

    files_to_process = get_files_to_process(rootnames)
    for input_file in files_to_process:
        add_s_region(input_file, dry_run)
    return

def get_files_to_process(rootnames):
    """Create a list of files to process from the list of rootnames

    """

    endings = ['rawtag.fits',
               'rawtag_a.fits',
               'rawtag_b.fits',
               'rawaccum.fits',
               'rawaccum_a.fits',
               'rawaccum_b.fits',
               'rawacq.fits']
    file_list = []
    for rootname in rootnames:
        fitslist = glob.glob(rootname.lower() + '*.fits')
        for input_file in fitslist:
            for ending in endings:
                if input_file.endswith(ending):
                    file_list.append(input_file)
    return file_list

def add_s_region(input_file, dry_run):
    """Add the computed S_REGION to the keyword
    """

    open_mode = 'readonly'
    if not dry_run: open_mode = 'update'

    with fits.open(input_file, mode=open_mode) as f1:
        prihdr = f1[0].header
        if prihdr['INSTRUME'] != 'COS':
            cosutil.printWarning("File {}: Instrument is not COS".format(file))
            return
        success = False
        for n_ext, extension in enumerate(f1[1:]):
            exthdr = extension.header
            extname = exthdr['EXTNAME']
            extver = exthdr['EXTVER']
            if extname in ['SCI', 'EVENTS', 'ACQ']:
                try:
                    ra_aper = exthdr['RA_APER']
                    dec_aper = exthdr['DEC_APER']
                    pa_aper = exthdr['PA_APER']
                except KeyError:
                    cosutil.printWarning('One or more of RA_APER, DEC_APER, PA_APER is not present')
                    cosutil.printContinuation('in extension {} header of file {}'.format(n_ext+1, input_file))
                    continue
                diameter = 2.5 / 3600.0
                s_region = 'CIRCLE ICRS {0:.8f} {1:.7f} {2:.8f}'.format(ra_aper, dec_aper, diameter)
                if not dry_run:
                    try:
                        existing_s_region = exthdr['S_REGION']
                        exthdr['S_REGION'] = s_region
                        cosutil.printMsg("Using existing S_REGION keyword in {}[{}, {}]".format(input_file, extname, extver))
                    except KeyError:
                        exthdr.insert('PA_APER', ('S_REGION', s_region, 'Spatial extent of the observation'), after=True)
                        cosutil.printMsg('Added S_REGION keyword to {}[{}, {}]'.format(input_file, extname, extver))
                    cosutil.printMsg("Setting value to '{}'".format(s_region))
                else:
                    cosutil.printMsg("S_REGION for {}[{}, {}] = '{}'".format(input_file, extname, extver, s_region))
                    cosutil.printMsg("Dry-run - no changes made to science header")
                success = True
        if not success:
            cosutil.printMsg('No S_REGION keyword added to file {}'.format(input_file))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
    """Add S_REGION value to raw data headers"""
    )

    parser.add_argument('rootnames', nargs='+',
        help='Rootnames to be processed')

    parser.add_argument(
        '--dry_run', action='store_true',
        help="Calculate S_REGION value, but don't write to data header[s]")

    args = parser.parse_args()
    main(args.rootnames, dry_run=args.dry_run)
