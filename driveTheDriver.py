#!/usr/bin/python

import numpy as np
import os

imgsize = ['DIY','GEO']

print '#!/bin/csh'
print ' '
for i in range(366):
	imgday = str(i+1)
	for j in range(len(imgsize)):
		cmd = "python SevereDriver.py "+imgday+" "+imgsize[j]
		print cmd
		#os.system(cmd)

print ' '
print 'exit'