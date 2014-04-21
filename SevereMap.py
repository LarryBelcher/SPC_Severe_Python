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

day_number = int(sys.argv[1]) #e.g., 1 through 366
data_index = day_number - 1
firstday = datetime.date(2008,1,1)
first_ordinal = firstday.toordinal()
day_ordinal = first_ordinal - 1 + day_number
this_date = datetime.date.fromordinal( day_ordinal )
mms = int2month(this_date.month)
dd = str(this_date.day)
mmdd = mms+' '+dd

imgsize = sys.argv[2]   #(expects 620, 1000, DIY, HD, or HDSD)

# Read Data
f = np.load('./Data/allsevere.npz')
lons = f['lons']
lats = f['lats']
probs = f['probs']
del f

path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS.ttf'
propr = font_manager.FontProperties(fname=path)
path = '/usr/local/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf'
propb = font_manager.FontProperties(fname=path)

if(imgsize == '620'):
	figxsize = 8.62
	figysize = 5.56
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 566
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_620_BaseLayer.png'
	line_img = './CONUS_620_stateLines.png'
	bgcol = '#F5F5F5'

if(imgsize == '1000'):
	figxsize = 13.89
	figysize = 8.89
	figdpi = 72
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo_42.png'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_1000_BaseLayer.png'
	line_img = './CONUS_1000_stateLines.png'
	bgcol = '#F5F5F5'

if(imgsize == 'DIY'):
	figxsize = 13.655
	figysize = 8.745
	figdpi = 300
	lllon, lllat, urlon, urlat = [-119.8939, 21.6678, -62.3094, 49.1895]
	logo_image = './noaa_logo.eps'
	logo_x = 946
	logo_y = 4
	framestat = 'False'
	base_img = './CONUS_DIY_BaseLayer.png'
	line_img = './CONUS_DIY_stateLines.png'
	bgcol = '#F5F5F5'

if(imgsize == 'HD'):
	figxsize = 21.33
	figysize = 10.25
	figdpi = 72
	lllon, lllat, urlon, urlat = [-123.89399, 19.66787, -53.30945, 48.18950]
	logo_image = './noaa_logo_100.png'
	logo_x = 1426
	logo_y = 29
	framestat = 'True'
	base_img = './CONUS_HD_BaseLayer.png'
	line_img = './CONUS_HD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'

if(imgsize == 'HDSD'):
	figxsize = 16
	figysize = 9.75
	figdpi = 72
	lllon, lllat, urlon, urlat = [-120.8000, 19.5105, -57.9105, 48.9905]
	logo_image = './noaa_logo_100.png'
	logo_x = 1042
	logo_y = 29
	framestat = 'True'
	base_img = './CONUS_HDSD_BaseLayer.png'
	line_img = './CONUS_HDSD_stateLines.png'
	framestat = 'False'
	bgcol = '#F5F5F5'


fig = plt.figure(figsize=(figxsize,figysize))
# create an axes instance, leaving room for colorbar at bottom.
ax1 = fig.add_axes([0.0,0.0,1.0,1.0], frameon=framestat)#, axisbg=bgcol)
ax1.spines['left'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)

# Create Map and Projection Coordinates
kwargs = {'epsg' : 5070,
          'resolution' : 'i',
          'llcrnrlon' : lllon,
          'llcrnrlat' : lllat,
          'urcrnrlon' : urlon,
          'urcrnrlat' : urlat,
          'lon_0' : -96.,
          'lat_0' : 23.,
          'lat_1' : 29.5,
          'lat_2' : 45.5,
		  'area_thresh' : 15000,
		  'ax' : ax1,
		  'fix_aspect' : False
}

#Set up the Basemap
m =Basemap(**kwargs)


#Add the BaseLayer image 1st pass
outline_im = Image.open(base_img)
m.imshow(outline_im, origin='upper', aspect='auto')


xx, yy = m(lons, lats)
levs = np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) / 100.
norm = colors.Normalize(levs[0], levs[-1])

#Define the color palette
cmap = plt.cm.YlOrRd

#Import the Brewer color palette (from CPT City
#cdict1 = gmtColormap('./CPT/BuPu_09.cpt')
#cmap = LinearSegmentedColormap('this_cmap', cdict1)

cdat = m.contourf(xx, yy, probs[data_index], levs, ax=ax1, cmap=cmap, norm=norm, alpha=0.55)
#call contourf again to eliminate lines (some magic I dug up form google, seems to work...)
cdat1 = m.contourf(xx, yy, probs[data_index], levs, ax=ax1, cmap=cmap, norm=norm, alpha=0.55)


#Add the Line image
outline_im = Image.open(line_img)
m.imshow(outline_im, origin='upper', alpha=0.75, zorder=10, aspect='auto')


#Add the NOAA logo (except for DIY)
if(imgsize != 'DIY'):
	logo_im = Image.open(logo_image)
	height = logo_im.size[1]
	# We need a float array between 0-1, rather than
	# a uint8 array between 0-255 for the logo
	logo_im = np.array(logo_im).astype(np.float) / 255
	fig.figimage(logo_im, logo_x, logo_y, zorder=10)



outpng = "temporary_map.png"

if(imgsize == '620' or imgsize == '1000' or imgsize == 'DIY'):
	plt.savefig(outpng,dpi=figdpi, orientation='landscape', bbox_inches='tight', pad_inches=0.00)

if(imgsize == 'HD' or imgsize =='HDSD'):
	plt.savefig(outpng, dpi=figdpi, orientation='landscape')#, bbox_inches='tight', pad_inches=0.01)


