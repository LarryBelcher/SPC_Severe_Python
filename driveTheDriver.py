#!/usr/bin/python

import numpy as np
import os

imgsize = '620'

for i in range(365):
	imgday = str(i+1)
	cmd = "python SevereDriver.py "+imgday+" "+imgsize
	print cmd
	#os.system(cmd)