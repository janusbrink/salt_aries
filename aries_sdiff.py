#!/usr/bin/env python
import sys
import numpy as np
import scipy.stats as st

from ccdproc import CCDData
import pylab as pl

def sdiff(
        afile,
        bfile,
        yc=120,
        dy=30,
        bg1=200,
        bg2=315,
        headertxt='5500',
        wc=5500,
        dw=-0.7,
        xsum=1,
        save=None,
        plot=True,
        ):
#   print '--%s %s--' % (afile, bfile)

    accd = CCDData.read(afile)
    bccd = CCDData.read(bfile)
    
    y1 = yc - dy
    y2 = yc + dy
    bg1 = bg1
    bg2 = bg2
    xbin = xsum

    # extract signal
    aspec = (accd.data[y1:y2,:] - np.median(accd.data[bg1:bg2,:], axis=0)).sum(axis=0) 
    bspec = (bccd.data[y1:y2,:] - np.median(bccd.data[bg1:bg2,:], axis=0)).sum(axis=0)
    rspec = bspec/aspec

    # apply spectral binning
    abin = aspec.reshape(-1,xbin)
    bbin = bspec.reshape(-1,xbin)
    rbin = rspec.reshape(-1,xbin)

    # estimate variance from counts per bin
    # sigma-clip data in each bin for variance calc
    #v = np.apply_along_axis(st.sigmaclip, 1, abin, low=3.0, high=3.0)
    #avar = np.array([np.var(x) for x in v[:,0]])
    #v = np.apply_along_axis(st.sigmaclip, 1, bbin, low=3.0, high=3.0)
    #bvar = np.array([np.var(x) for x in v[:,0]])

    # estimate variance from ratio per bin
    c = np.apply_along_axis(st.sigmaclip, 1, rbin, low=3.0, high=3.0)
    rvar = 2.0/xbin*np.array([np.var(x) for x in c[:,0]])

    # perform sigma clipping on bins
    c = np.apply_along_axis(st.sigmaclip, 1, abin, low=3.0, high=3.0)
    aspec = np.array([np.mean(x) for x in c[:,0]])
    c = np.apply_along_axis(st.sigmaclip, 1, bbin, low=3.0, high=3.0)
    bspec = np.array([np.mean(x) for x in c[:,0]])
    #aspec = abin.mean(axis=1)
    #bspec = bbin.mean(axis=1)
    rspec = bspec/aspec

    # extract variance
#    accdv = np.nan_to_num(accd.uncertainty.array)
#    bccdv = np.nan_to_num(bccd.uncertainty.array)
#    avar = accdv[y1:y2,:].sum(axis=0)
#    bvar = bccdv[y1:y2,:].sum(axis=0)
#    avar = avar.reshape(-1,xbin).mean(axis=1)
#    bvar = bvar.reshape(-1,xbin).mean(axis=1)

    xarr = np.arange(len(aspec))
    warr = (wc + xbin/2) + dw*xbin*xarr

    print 'ave = %f %%' % (rspec.mean()*100.0)
    print 'stdev = %f %%' % (rspec.std()*100.0)
    print 'range = %f %%' % ((rspec.max() - rspec.min())*100.0)
    #print 'S/N = %f / %f = %f' % (aspec.mean(), avar.mean(), aspec.mean()/avar.mean())

    if save:
        oarr = np.array([warr, aspec, bspec, rspec, rvar]).T
        oarr = oarr[oarr[:,0].argsort()]
        hdrtxt = "" # "\n%s\t%s\t%s\nwavelength [A]\trefspec [counts]\tcompspec [counts]\n" % (headertxt, afile, bfile)
        np.savetxt(save, oarr, fmt="%10e", delimiter="\t", header=hdrtxt)

    if plot:
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

if __name__ == '__main__':
    sdiff(*sys.argv[1:])
