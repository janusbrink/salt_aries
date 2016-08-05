import os, sys
import numpy as np
import argparse

from ccdproc import CCDData
#from pyhrs import red_process

import specutils
from astropy import units as u

from astropy import modeling as mod
from astropy.io import fits

import pylab as pl

import specreduce
from specreduce.models import ISISModel

from specreduce.interidentify import InterIdentify
from specreduce import spectools as st
from specreduce import WavelengthSolution


#Xe_spec = specutils.io.read_ascii.read_ascii_spectrum1d('Xe.salt', dispersion_unit=u.angstrom)


parser = argparse.ArgumentParser(description='Reduce arc data from SALT Engineering Aries Observations')
parser.add_argument('arcfile', help='an arcfile to wavelength calibrate')
parser.add_argument('--list', dest='arc_ref', default='CuArNe.txt', 
                   help='File with list of known arc lines')
parser.add_argument('--yc', dest='yc', default=121, type=int,
                   help='Row to extract')

args = parser.parse_args()
arcfile=args.arcfile
arc = fits.open(arcfile)

#read in arc lines
arc_ref=args.arc_ref
slines, sfluxes = np.loadtxt(arc_ref, usecols=(0,1), unpack=True)

function='poly'
order=1
rstep=1
nrows=1
mdiff=20
wdiff=3
thresh=3
niter=5
dc=3
ndstep=50
dsigma=5
method='Zeropoint'
res=6.0
dres=0.1
filename=None
smooth=0
inter=True
subback=0
textcolor='black'
log = None




data = arc[0].data
xarr = np.arange(data.shape[1])
warr = 4000 *u.angstrom +  4 * xarr * u.angstrom
#warr = rss.get_wavelength(xarr) * u.mm
#warr = warr.to(u.angstrom)

yc = args.yc
lmax = data[yc].max()
swarr, sfarr = st.makeartificial(slines, sfluxes, lmax, res, dres)
pl.plot(warr, data[yc])
mask = (swarr > warr.value.min()) * ( swarr < warr.value.max())
pl.plot(swarr[mask], sfarr[mask])
#pmel.show()
#nws = fit_ws(ws_init, xarr, warr)


ws_init = mod.models.Legendre1D(3)
ws_init.domain = [xarr.min(), xarr.max()]
ws = WavelengthSolution.WavelengthSolution(xarr, warr.value, ws_init)
ws.fit()

istart = yc
smask = (slines > warr.value.min()-20) * (slines < warr.value.max()+20)
iws = InterIdentify(xarr, data, slines[smask], sfluxes[smask], ws, mdiff=mdiff, rstep=rstep,
              function=function, order=order, sigma=thresh, niter=niter, wdiff=wdiff,
              res=res, dres=dres, dc=dc, ndstep=ndstep, istart=istart,
              method=method, smooth=smooth, filename=filename,
              subback=subback, textcolor=textcolor, log=log, verbose=True)

import pickle
name = os.path.basename(arcfile).replace('fit', 'pkl')
pickle.dump(iws, open(name, 'w'))

exit()

ws_init = mod.models.Legendre1D(3)
ws_init.domain = [xarr.min(), xarr.max()]
ws = WavelengthSolution.WavelengthSolution(xarr, xarr, ws_init)
ws.fit()
istart = arg.yc
aws = st.arc_straighten(data, istart, ws, rstep=1)

data = st.wave_map(data, aws)
k = iws.keys()[0]
for i in range(data.shape[0]):
    data[i,:] = iws[k](data[i,:])

arc.append(fits.ImageHDU(data=data, name='WAV'))
arc.writeto('w_' + os.path.basename(arcfile), clobber=True)

exit()

