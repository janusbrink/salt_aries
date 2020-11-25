#!/usr/bin/env python
import sys
import argparse
import numpy as np
import scipy.signal as sig
import scipy.stats as st

from ccdproc import CCDData
import pylab as pl

from aries_wcal import wcaldict
from aries_roi import roi

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is not one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[(window_len/2):-(window_len/2)]

def splot(
        infile,
        yc=roi['yc'],
        dy=roi['dy'],
        bg1=roi['bg1'],
        bg2=roi['bg2'],
        wref=None,
        wc=550,
        dw=-0.07,
        xsum=1,
        floor=1.01,
        save=False,
        noplot=False
        ):

    print infile

    accd = CCDData.read(infile)

    y1 = yc - dy
    y2 = yc + dy
    bg1 = bg1
    bg2 = bg2
    xbin = xsum

    print yc, dy, bg1, bg2

    # extract signal
    aspec = (accd.data[y1:y2,:] - np.median(accd.data[bg1:bg2,:], axis=0)).sum(axis=0)

    # apply spectral binning
    abin = aspec.reshape(-1,xbin)

    subpix = 10

    # perform sigma clipping on bins
    #c = np.apply_along_axis(st.sigmaclip, 1, abin, low=3.0, high=3.0)
    #aspec = np.array([np.mean(x) for x in c[:,0]])
    aspec = abin.mean(axis=1)

    if wref:
        wc = wcaldict[wref][0]
        dw = wcaldict[wref][1]
    xarr = np.arange(len(aspec)*subpix)
    warr = wc + (dw/subpix)*xbin*xarr

    # sub-pixel interpolate data
    i = 0
    ispec = np.ones(len(aspec)*subpix)
    for pval in aspec:
        ispec[i*subpix:(i+1)*subpix]=pval
        i = i + 1

    # mask noise
    ispec = smooth(ispec, window_len=2*subpix+1)
    cutoff = aspec.mean()*floor
    mask = ispec > cutoff
    pspec = ispec*mask
    peaks = sig.argrelmax(pspec, order = subpix)
    print warr[peaks]

    if save:
        oarr = np.array([warr[peaks], pspec[peaks]]).T
        #oarr = oarr[oarr.argsort()]
        hdrtxt = "" # "wavelength [nm]\trefspec [counts]\n"
        np.savetxt(save, oarr, fmt="%10e", delimiter="\t", header=hdrtxt)

    if not noplot:
        pl.figure()
        pl.subplot(111)
        pl.plot(warr, pspec)
        pl.ylabel('Counts', size='x-large')
        pl.xlabel('Wavelength', size='x-large')
        pl.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Aries engineering observationss')
    parser.add_argument('infile', nargs='*', help='File or files to be processed')
    parser.add_argument('--yc', help='Central row of object', type=int, default=107)
    parser.add_argument('--dy', help='Half width of object', type=int, default=30)
    parser.add_argument('--bg1', help='background region start', type=int, default=200)
    parser.add_argument('--bg2', help='background region end', type=int, default=315)
    parser.add_argument('--wref', help='wavelength reference', type=int, default=None)
    parser.add_argument('--wc', help='Central wavelength', type=float, default=1.0)
    parser.add_argument('--dw', help='Dispersion scale', type=float, default=1.0)
    parser.add_argument('--xsum', help='spectral smooth box size', type=int, default=1)
    parser.add_argument('--floor', help='Noise cut-off ratio', type=float, default=1.0)
    parser.add_argument('--save', help='Save to file', type=str, default=None)
    parser.add_argument('--noplot', help='Suppress plotting', action="store_true")
    args = parser.parse_args()

    fnum = 1
    for fil in args.infile:
       if args.save:
           fname = args.save + "_%03d.txt" % fnum
       else:
           fname = None
       splot(fil, args.yc, args.dy, args.bg1, args.bg2, args.wref, args.wc, args.dw, args.xsum, args.floor, fname, args.noplot)
       fnum = fnum + 1
