#!/usr/bin/python

import numpy as np
import os

imgsize = 'HDSD'

print '#!/bin/csh'
print ' '
for i in range(366):
	imgday = str(i+1)
	cmd = "python SevereDriver.py "+imgday+" "+imgsize
	print cmd
	#os.system(cmd)

print ' '
print 'exit'