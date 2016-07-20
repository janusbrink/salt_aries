import sys
import os
import numpy as np
from aries_sdiff import sdiff  

import argparse

parser = argparse.ArgumentParser(description='Process Aries engineering observationss')
parser.add_argument('infile', nargs='*', help='File or files to be processed')
args = parser.parse_args()


infiles = args.infile

if len(infiles) % 2 != 0:
   print 'WARNING: expected an even number of files'
   del infiles[-1]

inarr = np.array(infiles)
inarr = inarr.reshape(-1,2)

for fileset in inarr:
   print '[%s %s]' % (fileset[0], fileset[1])
   sdiff(fileset[0], fileset[1])
