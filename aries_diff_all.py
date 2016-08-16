import numpy as np
from aries_sdiff import sdiff
import argparse

from aries_wcal import wcaldict

# test configuration
#           ref    cmp   wavelength [A]
#cfglist = (
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    ('out', 'in', 5500),
#    )

cfglist = (
    ('out', 'in', 3500),
    ('out', 'in', 4000),
    ('out', 'in', 4500),
    ('out', 'in', 5000),
    ('out', 'in', 5500),
    ('out', 'in', 6000),
    ('out', 'in', 6500),
    ('out', 'in', 7000),
    ('out', 'in', 7500),
    ('out', 'in', 8000),
    ('out', 'in', 8500),
    ('out', 'in', 9000)
    )

parser = argparse.ArgumentParser(description='Process Aries engineering observationss')
parser.add_argument('infile', nargs='*', help='File or files to be processed')
parser.add_argument('--plot', help='Plot graphs', action = "store_true")
parser.add_argument('--dryrun', help='Do not write output files', action = "store_true")
parser.add_argument('--xsum', help='Spatial binning size', type = int, default = 50)
args = parser.parse_args()

infiles = args.infile

if len(infiles) % 2:
    print 'WARNING: expected an even number of files'
    del infiles[-1]

flist = np.array(infiles)
flist = flist.reshape(-1, 2)

# iterate over file pairs, obtaining cfg and wcal from tables above
i = 0
for fil, cfg in zip(flist, cfglist):
    fname = 'throughput%02d_%d.txt' % (i, cfg[2])
    reffile = fil[cfg.index('out')]
    cmpfile = fil[cfg.index('in')]
    wcal = wcaldict[cfg[2]]
    if args.dryrun:
        fname = None
    print '\n**%s, %s >> %s' % (reffile, cmpfile, fname)
    sdiff(reffile, cmpfile, headertxt=cfg[2], wc=wcal[0], dw=wcal[1], plot=args.plot, xsum=args.xsum, save=fname)
    i = i + 1
