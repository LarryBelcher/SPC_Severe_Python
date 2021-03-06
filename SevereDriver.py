#!/usr/bin/python

import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, datetime, sys, subprocess, glob
import numpy as np



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


imgday = sys.argv[1]	#expects a day of year, e.g., 135
imgsize = sys.argv[2]	#(expects 620, 1000, DIY, HD, or HDSD)

day_number = int(sys.argv[1])
data_index = day_number - 1
firstday = datetime.date(2008,1,1)
first_ordinal = firstday.toordinal()
day_ordinal = first_ordinal - 1 + day_number
this_date = datetime.date.fromordinal( day_ordinal )
if(this_date.month << 10): mm = '0'+str(this_date.month)
if(this_date.month >= 10): mm = str(this_date.month)
mms = int2month(this_date.month)
if(this_date.day << 10): dd = '0'+str(this_date.day)
if(this_date.day >= 10): dd = str(this_date.day)
mmdd = mms+' '+dd

figdpi = 72

cmd = "python ./SevereMap.py "+imgday+" "+imgsize
os.system(cmd)

if(imgsize != 'GEO'):
	cmd = "python ./SevereColorbar.py "+imgday+" "+imgsize
	os.system(cmd)

if(imgsize != 'GEO'):
	if not os.path.isdir('./Images'):
		cmd = 'mkdir ./Images'
		os.system(cmd)
	if not os.path.isdir('./Images/'+imgsize.lower()):
		cmd = 'mkdir ./Images/'+imgsize.lower()
		os.system(cmd)


if(imgsize == '620' or imgsize == '1000'):
	im1 = Image.open("temporary_map.png")
	im2 = Image.open("temporary_cbar.png")
	im3 = Image.new('RGBA', size = (im1.size[0], im1.size[1]+im2.size[1]))
	im3.paste(im2, (0,im1.size[1]))
	im3.paste(im1, (0,0))
	img_path = './Images/'+imgsize.lower()+'/'
	imgw = str(im3.size[0])
	imgh = str(im3.size[1])
	img_name = 'probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'--0000-'+mm+'-'+dd+'.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	im3.save(pngfile)


if(imgsize == 'DIY'):
	im1 = "./temporary_map.png"
	imgs = Image.open(im1)
	imgw = str(imgs.size[0])
	imgh = str(imgs.size[1])
	img_path = './Images/'+imgsize.lower()+'/'
	img_name = 'probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'--0000-'+mm+'-'+dd+'.png'
	cmd = 'mv '+im1+' '+img_name
	subprocess.call(cmd, shell=True)
	im2 = "./temporary_cbar.eps"
	cbar_name = 'probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'--0000-'+mm+'-'+dd+'_colorbar.eps'
	cmd = 'mv '+im2+' '+cbar_name
	subprocess.call(cmd, shell=True)
	cmd1 = 'zip probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'--0000-'+mm+'-'+dd+'.zip '+img_name+' '+cbar_name+' noaa_logo.eps '
	subprocess.call(cmd1, shell=True)
	cmd2 = 'mv probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'--0000-'+mm+'-'+dd+'.zip '+img_path
	subprocess.call(cmd2, shell=True)
	cmd3 = 'rm '+img_name+' '+cbar_name
	subprocess.call(cmd3, shell=True)
	
if(imgsize == 'GEO'):
	im1 = "./temporary_map.tif"
	tifimgs = Image.open(im1)
	tifimgw = str(tifimgs.size[0])
	tifimgh = str(tifimgs.size[1])
	tifimg_name = 'probseverewx-dayofyear-spc--'+tifimgw+'x'+tifimgh+'--0000-'+mm+'-'+dd+'.tif'
	cmd = 'gdal_translate -of GTiff -a_srs EPSG:4326  -a_ullr -179.9853516 74.9853516 -59.9853516 14.9853516 '+im1+' '+tifimg_name
	subprocess.call(cmd,shell=True)
	zpath = './Images/diy/*0000-'+mm+'-'+dd+'.zip'
	zipfile = glob.glob(zpath)
	cmd = 'zip -u '+zipfile[0]+' '+tifimg_name
	subprocess.call(cmd,shell=True)
	cmd1 = 'rm '+tifimg_name
	subprocess.call(cmd1, shell=True)
	
	
if(imgsize == 'HD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1534,736)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (192,108))
	
	draw = ImageDraw.Draw(hdim)
	fntpath = './Fonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 37)
	draw.text((205,775), mmdd, (0,0,0), font=fnt1)
	fnt2 = ImageFont.truetype(fntpath, 14)
	ttext = "Based on storms from 1982-2011"
	draw.text((207,817), ttext, (0,0,0), font=fnt2)	
	
	#Add the colorbar
	cbar_orig = Image.open('temporary_cbar.png')
	bbox = (1,1,972,43)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_im, (474,865))
		
	fnt3 = ImageFont.truetype(fntpath, 37)
	text1 = "Historical Probability of Severe Weather"
	draw.text((625,915), text1, (0,0,0), font=fnt3)	
	fnt4 = ImageFont.truetype(fntpath, 24)
	text2 = "1%"
	draw.text((468,913), text2, (0,0,0), font=fnt4)
	text3 = "8%"
	draw.text((1435,913), text3, (0,0,0), font=fnt4)
	
	draw.polygon([(1300,949), (1315,939), (1300,929)], fill="black", outline="black")
	
	img_path = './Images/'+imgsize.lower()+'/'
	img_name = 'probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'hd--0000-'+mm+'-'+dd+'.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	hdim.save(pngfile)


if(imgsize == 'HDSD'):
	hdim = Image.new("RGB", (1920,1080), color='#FFFFFF')
	imgw = '1920'
	imgh = '1080'
	
	im1 = Image.open("temporary_map.png")
	bbox = (0,0,1150,700)
	im1 = im1.crop(bbox)
	osize = im1.size
	new_size = (osize[0]+2,osize[1]+2)
	im1new = Image.new("RGB", new_size)
	im1new.paste(im1, ((new_size[0]-osize[0])/2, (new_size[1]-osize[1])/2))
		
	hdim.paste(im1new, (384,108))
	
	draw = ImageDraw.Draw(hdim)
	fntpath = './Fonts/Trebuchet_MS.ttf'
	fnt1 = ImageFont.truetype(fntpath, 37)
	draw.text((397,739), mmdd, (0,0,0), font=fnt1)
	fnt2 = ImageFont.truetype(fntpath, 14)
	ttext = "Based on storms from 1982-2011"
	draw.text((399,781), ttext, (0,0,0), font=fnt2)	
	
	#Add the colorbar
	cbar_orig = Image.open('temporary_cbar.png')
	bbox = (1,1,972,43)
	cbar_orig = cbar_orig.crop(bbox)
	old_size = cbar_orig.size
	new_size = (old_size[0]+2,old_size[1]+2)
	cbar_im = Image.new("RGB", new_size)
	cbar_im.paste(cbar_orig, ((new_size[0]-old_size[0])/2,
                      (new_size[1]-old_size[1])/2))
	hdim.paste(cbar_im, (474,830))
		
	fnt3 = ImageFont.truetype(fntpath, 37)
	text1 = "Historical Probability of Severe Weather"
	draw.text((625,880), text1, (0,0,0), font=fnt3)	
	fnt4 = ImageFont.truetype(fntpath, 24)
	text2 = "1%"
	draw.text((468,878), text2, (0,0,0), font=fnt4)
	text3 = "8%"
	draw.text((1435,878), text3, (0,0,0), font=fnt4)
	
	draw.polygon([(1300,914), (1315,904), (1300,894)], fill="black", outline="black")
	
	img_path = './Images/'+imgsize.lower()+'/'
	img_name = 'probseverewx-dayofyear-spc--'+imgw+'x'+imgh+'hdsd--0000-'+mm+'-'+dd+'.png'
	pngfile = img_path+img_name
	print "Saving "+pngfile
	hdim.save(pngfile)