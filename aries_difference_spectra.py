import sys
import os
  
import argparse
from aries_sdiff import sdiff

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

sdiff(args.afile, args.bfile, yc = args.yc, dy = args.dy,
   bg1 = args.bg1, bg2 = args.bg2,
   wc = args.wc, dw = args.dw,
   xsum = args.xsum, save = args.save, noplot = args.noplot)
