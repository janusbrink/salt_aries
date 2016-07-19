import sys
import os
import numpy as np
  
from astropy.io import fits
from astropy import units as u

import ccdproc 
from ccdproc import CCDData

import argparse
import pylab as pl


parser = argparse.ArgumentParser(description='Create a 1-D difference spectrum')
parser.add_argument('afile', help='Reference file for spectra')
parser.add_argument('bfile', help='File to be compared')
parser.add_argument('--yc', help='Central row of object', type=int, default=120)
parser.add_argument('--dy', help='Half width of object', type=int, default=30)
parser.add_argument('--bg1', help='background region start', type=int, default=200)
parser.add_argument('--bg2', help='background region end', type=int, default=315)
parser.add_argument('--wc', help='Central wavelength', type=float, default=1.0)
parser.add_argument('--dw', help='Dispersion scale', type=float, default=1.0)
parser.add_argument('--xsum', help='spectral smooth box size', type=int, default=50)
parser.add_argument('--save', help='Save to file', type=str, default=None)
parser.add_argument('--noplot', help='Supress plotting', action = "store_true")
args = parser.parse_args()

accd = CCDData.read(args.afile)
bccd = CCDData.read(args.bfile)

y1 = args.yc - args.dy
y2 = args.yc + args.dy
bg1 = args.bg1
bg2 = args.bg2
xbin = args.xsum

aspec = (accd.data[y1:y2,:] - np.median(accd.data[bg1:bg2,:], axis=0)).sum(axis=0) 
bspec = (bccd.data[y1:y2,:] - np.median(bccd.data[bg1:bg2,:], axis=0)).sum(axis=0)

aspec = aspec.reshape(-1,xbin).mean(axis=1)
bspec = bspec.reshape(-1,xbin).mean(axis=1)
rspec = bspec/aspec - 1.0

xarr = np.arange(len(aspec))
warr = (args.wc + xbin/2) + args.dw*xbin*xarr

print 'ave = %f %%' % (rspec.mean()*100.0)
print 'stdev = %f %%' % (rspec.std()*100.0)
print 'range = %f %%' % ((rspec.max() - rspec.min())*100.0)

if args.save != None:
   oarr = np.array([warr, bspec, aspec])
   np.savetxt(args.save, oarr.T, fmt="%f", delimiter="\t")

if args.noplot == False:
   pl.figure()
   pl.subplot(311)
   pl.plot(warr, aspec)
   pl.plot(warr, bspec)
   pl.ylabel('Counts', size='x-large')
   pl.subplot(312)
   pl.plot(warr, bspec-aspec)
   pl.ylabel('Diff', size='x-large')
   pl.subplot(313)
   pl.plot(warr, rspec*100.0)
   pl.ylabel('Deviation (%)', size='x-large')
   pl.xlabel('Wavelength', size='x-large')
   pl.show()

