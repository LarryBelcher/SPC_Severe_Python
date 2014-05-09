#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
import os, datetime, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.font_manager as font_manager
from PIL import Image


def int2month(mmi):
	if(mmi == 1): mms = 'January'
	if(mmi == 2): mms = 'February'
	if(mmi == 3): mms = 'March'
	if(mmi == 4): mms = 'April'
	if(mmi == 5): mms = 'May'
	if(mmi == 6): mms = 'June'
	if(mmi == 7): mms = 'July'
	if(mmi == 8): mms = 'August'
	if(mmi == 9): mms = 'September'
	if(mmi == 10): mms = 'October'
	if(mmi == 11): mms = 'November'
	if(mmi == 12): mms = 'December'	
	return mms

day_number = int(sys.argv[1])
data_index = day_number - 1
firstday = datetime.date(2008,1,1)
first_ordinal = firstday.toordinal()
day_ordinal = first_ordinal - 1 + day_number
this_date = datetime.date.fromordinal( day_ordinal )
mms = int2month(this_date.month)
dd = str(this_date.day)
mmdd = mms+' '+dd

imgsize = sys.argv[2]   #(expects 620, 1000, DIY, HD, or HDSD)

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
	figxsize = 8.62
	figysize = 0.695
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.1733; cbw = 0.652; cby = 0.34; cbh = 0.24
	t1x = 0.318; t1y = 0.665
	t2x = 0.685; t2y = 0.664
	t3x = 0.008; t3y = 0.77
	t4x = 0.899; t4y = 0.77
	t5x = 0.908; t5y = 0.55
	t9y = -1.0
	pngfile = "temporary_cbar.png"

if(imgsize == '1000'):
	figxsize = 13.89
	figysize = 0.695
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.2975; cbw = 0.4045; cby = 0.34; cbh = 0.24
	t1x = 0.387; t1y = 0.665
	t2x = 0.615; t2y = 0.664
	t3x = 0.004; t3y = 0.77
	t4x = 0.938; t4y = 0.77
	t5x = 0.944; t5y = 0.55
	t9y = -1.0
	pngfile = "temporary_cbar.png"

if(imgsize == 'DIY'):
	figxsize = 8.89
	figysize = 2.44
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.185; cbw = 0.63; cby = 0.38; cbh = 0.1
	t1x = 0.33; t1y = 0.565
	t2x = 0.69; t2y = 0.565
	t3x = 0.05; t3y = 0.82
	t4x = 0.85; t4y = 0.82
	t5x = 0.86; t5y = 0.63
	t9y = -0.7
	pngfile = "temporary_cbar.eps"

if(imgsize == 'HD' or imgsize == 'HDSD'):
	figxsize = 13.5
	figysize = 0.611
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	cbx = 0.0; cbw = 1.0; cby = 0.01; cbh = 0.99
	t1x = 0.33; t1y = 0.565
	t2x = 0.69; t2y = 0.565
	t3x = 0.05; t3y = 0.82
	t4x = 0.85; t4y = 0.82
	t5x = 0.86; t5y = 0.63
	pngfile = "temporary_cbar.png"

fig = plt.figure(figsize=(figxsize,figysize))

# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0,0.0,1.0,1.0], axisbg='#F5F5F5')
ax1.set_frame_on(False)
ax1.set_xticks([])
ax1.set_xticklabels([])
ax1.set_yticks([])
ax1.set_yticklabels([])


if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	dval = "Historical Probability of Severe Weather"
	plt.text(t1x, t1y, dval, fontproperties=propb, size=fsiz1, color='#333333')
	plt.text(t2x, t2y, "(%)", fontproperties=propr, size=fsiz1, color='#333333')

	plt.text(t3x, t3y, mmdd, fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t4x, t4y, 'Climate.gov', fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t5x, t5y, 'Data: SPC', fontproperties=propr, size=fsiz2, color='#8D8D8D')

#Define the color palette
cmap = plt.cm.YlOrRd
levs = np.asarray([1, 2, 3, 4, 5, 6, 7, 8]) / 100.
#norm = colors.Normalize(levs[0], levs[-1])
norm = mpl.colors.BoundaryNorm(levs, cmap.N)
ax2 = fig.add_axes([cbx,cby,cbw,cbh], axisbg='#F5F5F5')
ax2.set_frame_on(False)
ax2.set_xticks([])
ax2.set_xticklabels([])
ax2.set_yticks([])
ax2.set_yticklabels([])

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	#ax2.text(0.88, t9y , r'9', fontsize=fsiz2)
	barticks = (np.arange(8)+1)/100.
	barlevs = ['1', '2', '3', '4', '5', '6', '7', '8']
	bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	bar.outline.set_visible(True)
	bar.outline.set_linewidth(0.6)
	bar.ax.tick_params(size=0.01)
	bar.ax.set_xticklabels(barlevs, fontproperties=propr, size=fsiz2, va='top')

if(imgsize == 'HD' or imgsize == 'HDSD'):
	barticks = (np.arange(8)+1)/100.
	barlevs = ['', '', '', '', '', '', '','']
	bar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal', ticks=barticks)
	bar.outline.set_visible(True)
	bar.outline.set_linewidth(0.6)
	bar.ax.tick_params(size=0.01)
	bar.ax.set_xticklabels(barlevs, fontproperties=propr, size=fsiz2, va='top')

if(imgsize != 'DIY'):
	plt.savefig(pngfile, dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.0)

if(imgsize == 'DIY'):
	plt.savefig(pngfile, dpi=figdpi, orientation='portrait', bbox_inches='tight', pad_inches=0.0)