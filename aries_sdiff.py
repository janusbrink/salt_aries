import sys
import os

import numpy as np

from astropy.io import fits
from astropy import units as u

import ccdproc 
from ccdproc import CCDData

import pylab as pl

def sdiff(afile, bfile, yc = 120, dy = 30, bg1 = 200, bg2 = 315, headertxt = '5500', wc = 5500, dw = -0.7, xsum = 1, save = None, noplot = False):
#   print '--%s %s--' % (afile, bfile)

   accd = CCDData.read(afile)
   bccd = CCDData.read(bfile)

   y1 = yc - dy
   y2 = yc + dy
   bg1 = bg1
   bg2 = bg2
   xbin = xsum

   aspec = (accd.data[y1:y2,:] - np.median(accd.data[bg1:bg2,:], axis=0)).sum(axis=0) 
   bspec = (bccd.data[y1:y2,:] - np.median(bccd.data[bg1:bg2,:], axis=0)).sum(axis=0)

   aspec = aspec.reshape(-1,xbin).mean(axis=1)
   bspec = bspec.reshape(-1,xbin).mean(axis=1)
   rspec = bspec/aspec - 1.0

   xarr = np.arange(len(aspec))
   warr = (wc + xbin/2) + dw*xbin*xarr

   print 'ave = %f %%' % (rspec.mean()*100.0)
   print 'stdev = %f %%' % (rspec.std()*100.0)
   print 'range = %f %%' % ((rspec.max() - rspec.min())*100.0)

   if save != None:
      oarr = np.array([warr, aspec, bspec]).T
      oarr = oarr[oarr[:,0].argsort()]
      hdrtxt = "" # "\n%s\t%s\t%s\nwavelength [A]\trefspec [counts]\tcompspec [counts]\n" % (headertxt, afile, bfile)
      np.savetxt(save, oarr, fmt="%f", delimiter="\t", header=hdrtxt)

   if noplot == False:
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

