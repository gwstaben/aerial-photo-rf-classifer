#!/usr/bin/env python

"""
Script to clip multiple raster images based on shapefiles which define the extent. 

Code to produce the csv or txt file requried is located in the jupyter notebook Aerial_photo_class_workflow.ipynb 

example of the expected csv or txt file shown below which includes a header and rows:
            
            'img','shp'
            C:/DATA/todd/example/asp_2015_15cm_02_wgs84.tif, C:/DATA/todd/example/shp/grd_50m4_ID01.shp
            C:/DATA/todd/example/asp_2015_15cm_02_wgs84.tif, C:/DATA/todd/example/shp/grd_50m4_ID02.shp
            C:/DATA/todd/example/asp_2015_15cm_02_wgs84.tif, C:/DATA/todd/example/shp/grd_50m4_ID03.shp

# This script is written to run on the py3k environment. 

Grant Staben
17/07/2019

###############################################################################################

MIT License

Copyright (c) 2022 Grant Staben

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

###############################################################################################

Parameters: 
-----------

list : csv or text file 
            csv file containing the image and shapefile defining the extent of the image to be clipped.
            
           
"""

import sys
import os
import argparse
import json
import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
import pandas as pd
from fiona.crs import from_epsg
#import pycrs

# define the paths to the PROJ lib and GDAL, this is needed when running on some NTG laptops
os.environ['PROJ_LIB'] = 'C:/ProgramData/Miniconda3/Library/share/proj'
os.environ['GDAL_DATA'] = 'C:/ProgramData/Miniconda3/Library/share'

#function to get cmd line inputs
def getCmdargs():
    
    p = argparse.ArgumentParser()
    
    p.add_argument("-i","--list", help="list of raster imagery and the corresponding shapefiles used to clip the raster")
    
   
    cmdargs = p.parse_args()
    
    if cmdargs.list is None:

        p.print_help()

        sys.exit()

    return cmdargs


def covShp(geo_dissovle):
    """
    Function to parse features from GeoDataFrame in such 
    a manner that rasterio wants them
    """
   
    return [json.loads(geo_dissovle.to_json())['features'][0]['geometry']]


def dissolveShp(inshp):
    
    """ 
    Function to dissolve the shapefile to enable 
    the extent of the shapefile to be parsed to
    the json file. 
    """
    # read in the shapefile
    geo = gpd.read_file(inshp)
    # create a new field to dissolve the individual shape into a single polygon
    geo['dis'] = 1
    # dissolve the individual polygons
    geo_dissolve = geo.dissolve(by='dis')
    
    return geo_dissolve


def epsg(epsg_code):
    
    """
    function to convert the epsg code to proj4, the orginal example of the code used pycrs 
    to obtain this infromatin for the internet. This version relies on it being in this function. 
    I have covered all the codes relevent to me however it may fail if used elsewhere.
    
    """
    if epsg_code == 32752:
        epsg_code_proj4 = '+proj=utm +zone=52 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    if epsg_code == 32753:
        epsg_code_proj4 = '+proj=utm +zone=53 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
        
    if epsg_code == 28352:
        epsg_code_proj4 = '+proj=utm +zone=52 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'   
    
    if epsg_code == 28353:
        epsg_code_proj4 = '+proj=utm +zone=53 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'        
    
    if epsg_code == 4283:
        epsg_code_proj4 = '+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs'     
        
    if epsg_code == 6644:
        epsg_code_proj4 = '+proj=aea +lat_1=-18 +lat_2=-36 +lat_0=0 +lon_0=134 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs' 
    if epsg_code == 3577:
        epsg_code_proj4 = '+proj=aea +lat_1=-18 +lat_2=-36 +lat_0=0 +lon_0=132 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'
    
    return epsg_code_proj4


def main():
    
    """
    Main routine
    
    """
    
    cmdargs = getCmdargs()
        
    # open the list of imagery and read it into memory
    df = pd.read_csv(cmdargs.list,header=0)
   
    for index, row in df.iterrows():
        inImage = (str(row['img']))
        inshp = (str(row['shp']))

        # create the output file name by removeing the .shp and replacing it with .tif
        out_tif = (str(row['shp'][:-4]) +'.tif')

        # read in the raster image to produce the clip rasters from
        data = rasterio.open(inImage)
        
        # function to dissolve any multi polygons
        geo_dissolve = dissolveShp(inshp)
        
        # get the extent of the shapefile    
        coords = covShp(geo_dissolve)
    
        # produce the clipped raster image
        out_img, out_transform = mask(data, coords, crop=True)
        
        # get the projection and datum form the input image and update the clip datas metadata
        
        epsg_code = int(data.crs.data['init'][5:])
        print (epsg_code)
        # select the relevent epsg code and convert it to proj4 format 
        epsg_code_proj4 = epsg(epsg_code)
       
        out_meta = data.meta.copy()

        out_meta.update({"driver": "GTiff","height": out_img.shape[1],"width": out_img.shape[2],"transform": out_transform,"crs": epsg_code_proj4})
    
        # write out the clipped raster image
        with rasterio.open(out_tif, "w", **out_meta) as dest:
            dest.write(out_img)
    
        # close the output raster image
        data.close()

if __name__ == "__main__":
    main()