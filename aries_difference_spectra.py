import argparse
from aries_sdiff import sdiff
from aries_wcal import wcaldict
from aries_roi import roi

parser = argparse.ArgumentParser(description='Create a 1-D difference spectrum')
parser.add_argument('afile', help='Reference file for spectra')
parser.add_argument('bfile', help='File to be compared')
parser.add_argument('--yc', help='Central row of object', type=int, default=roi['yc'])
parser.add_argument('--dy', help='Half width of object', type=int, default=roi['dy'])
parser.add_argument('--bg1', help='background region start', type=int, default=roi['bg1'])
parser.add_argument('--bg2', help='background region end', type=int, default=roi['bg2'])
parser.add_argument('--wc', help='Central wavelength', type=float, default=1.0)
parser.add_argument('--wref', help='wavelength reference', type=int, default=None)
parser.add_argument('--dw', help='Dispersion scale', type=float, default=1.0)
parser.add_argument('--xsum', help='spectral smooth box size', type=int, default=50)
parser.add_argument('--save', help='Save to file', type=str, default=None)
parser.add_argument('--noplot', help='Supress plotting', action = "store_true")
args = parser.parse_args()

if args.wref:
    _wc = wcaldict[args.wref][0]
    _dw = wcaldict[args.wref][1]
else:
    _wc = args.wc
    _dw = args.dw

sdiff(args.afile, args.bfile, yc=args.yc, dy=args.dy,
   bg1=args.bg1, bg2=args.bg2,
   wc=_wc, dw=_dw,
   xsum=args.xsum, save=args.save, plot=not args.noplot)
