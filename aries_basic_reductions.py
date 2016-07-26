import sys
import os
import numpy as np
  
from astropy import units as u

import ccdproc 
from ccdproc import CCDData

import argparse

parser = argparse.ArgumentParser(description='Process Aries engineering observationss')
parser.add_argument('infile', nargs='*', help='File or files to be processed')
parser.add_argument('--b', dest='bias', help='Master bias file', default=None)
parser.add_argument('--d', dest='dark', help='Master dark file', default=None)
parser.add_argument('--f', dest='flat', help='Master flat file', default=None)
parser.add_argument('-n', dest='cray', default=True, action='store_false', help='Do not cosmic ray clean')
args = parser.parse_args()

infiles = args.infile

print infiles

if args.bias:
   mbias = CCDData.read(args.bias, unit=u.adu)
else:
   mbias = None

if args.flat: 
   raise Exception('Flat fielding is not currently implemented')
if args.dark: 
   mdark = CCDData.read(args.dark, unit=u.adu)
else:
   mdark = None

for infile in infiles:
    ccd = CCDData.read(infile, unit=u.adu)
    if mdark:
        ccd = ccdproc.subtract_dark(ccd, mdark, exposure_time='EXPTIME', exposure_unit=u.second)
    ccd = ccdproc.ccd_process(ccd, oscan='[1121:1181, 1:330]', oscan_median=True, 
                              trim='[17:1116,1:330]', master_bias=mbias,
                              error=True, gain=1.0 * u.electron/u.adu, 
                              readnoise=5.0 * u.electron)
    if args.cray:
        ccd = ccdproc.cosmicray_lacosmic(ccd, sigclip=4.5, sigfrac=0.3,
                   objlim=5.0, gain=1.0, readnoise=6.5,
                   satlevel=4096.0, pssl=0.0, niter=4,
                   sepmed=True, cleantype='meanmask', fsmode='median',
                   psfmodel='gauss', psffwhm=2.5, psfsize=7,
                   psfk=None, psfbeta=4.765, verbose=False)
    ccd.write('p'+os.path.basename(infile), clobber=True)

