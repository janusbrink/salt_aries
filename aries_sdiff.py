#!/usr/bin/env python
import sys
import numpy as np
import scipy.stats as st

from ccdproc import CCDData
import pylab as pl

from aries_roi import roi

#like st.sigmaclip, but duplicates operation on noise array "n" as well.
def sigmaclip_n(
        a,
        n,
        low,
        high,
        ):

    mean_a = np.mean(a)
    std_a = np.std(a)

    c = np.arange(0)
    cn = np.array([])
    for i in range(np.shape(a)[0]):
        if (a[i] > (mean_a - std_a*low) and  a[i] < (mean_a + std_a*high)):
            c = np.append(c,a[i])
            cn = np.append(cn,n[i])

    return c, cn

# determine ratio between two spectra
# takes two image files and extracts spectra, subtracting the median of a beckground region for each
# signal is summed over the spatial 'height' (2 x dy), and the mean is computed per spectal bin
# (specified by xsum)
# shot noise error propagation is maintained throughout
def sdiff(
        afile,
        bfile,
        yc=roi['yc'],
        dy=roi['dy'],
        bg1=roi['bg1'],
        bg2=roi['bg2'],
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

    # extract signal - spatial binningl
    aspec = (accd.data[y1:y2,:] - np.median(accd.data[bg1:bg2,:], axis=0)).sum(axis=0)
    bspec = (bccd.data[y1:y2,:] - np.median(bccd.data[bg1:bg2,:], axis=0)).sum(axis=0)
    # error propagation
    avar = (accd.data[y1:y2,:]+np.median(accd.data[bg1:bg2,:], axis=0)*(bg2-bg1)/np.square(bg2-bg1)).sum(axis=0)
    bvar = (bccd.data[y1:y2,:]+np.median(bccd.data[bg1:bg2,:], axis=0)*(bg2-bg1)/np.square(bg2-bg1)).sum(axis=0)

    if (xbin > 1):
        # apply spectral binning
        abin = aspec.reshape(-1,xbin)
        bbin = bspec.reshape(-1,xbin)
        avbin = avar.reshape(-1,xbin)
        bvbin = bvar.reshape(-1,xbin)

        cols = abin.shape[0]
        a = []
        av = []
        for x in np.arange(cols):
            k, kn = sigmaclip_n(abin[x], avbin[x], low=3.0, high=3.0)
            a.extend([k])
            av.extend([kn])

        cols = bbin.shape[0]
        b = []
        bv = []
        for x in np.arange(cols):
            k, kn = sigmaclip_n(bbin[x], bvbin[x], low=3.0, high=3.0)
            b.extend([k])
            bv.extend([kn])

        aspec = np.array([np.mean(x) for x in a])
        bspec = np.array([np.mean(x) for x in b])

        #error propagation
        avar = np.array([x.sum()/np.square(np.shape(x)[0]) for x in av])
        bvar = np.array([x.sum()/np.square(np.shape(x)[0]) for x in bv])

    # spectral ratio
    rspec = bspec/aspec
    # error propagation
    rvar = np.square(rspec)*(avar/np.square(aspec) + bvar/np.square(bspec))

    #print rspec
    #print np.sqrt(rvar)

    xarr = np.arange(len(aspec))
    warr = (wc + xbin/2) + dw*xbin*xarr

    print 'ave = %f %%' % (rspec.mean()*100.0)
    print 'stdev = %f %%' % (rspec.std()*100.0)
    print 'range = %f %%' % ((rspec.max() - rspec.min())*100.0)
    print 'S/N(a) = %f / %f = %f' % (aspec.mean(), np.sqrt(avar).mean(), aspec.mean()/np.sqrt(avar).mean())
    print 'S/N(b) = %f / %f = %f' % (bspec.mean(), np.sqrt(bvar).mean(), bspec.mean()/np.sqrt(bvar).mean())
    print 'S/N(r) = %f / %f = %f' % (rspec.mean(), np.sqrt(rvar).mean(), rspec.mean()/np.sqrt(rvar).mean())

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
        pl.plot(warr, (rspec+np.sqrt(rvar))*100.0)
        pl.ylabel('Deviation (%)', size='x-large')
        pl.xlabel('Wavelength', size='x-large')
        pl.show()

if __name__ == '__main__':
    sdiff(*sys.argv[1:])
