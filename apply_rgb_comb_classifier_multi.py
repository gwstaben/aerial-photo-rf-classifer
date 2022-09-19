#!/usr/bin/env python

"""
This code applies a random forest classifer to predict a number of cover classes from 8 bit digital areial photogrpahy. The classifier
was trained on 15cm digital aerial photorgrpahy captured across the topend of the Northern Territory between the years 2008 to 2018. 

This script applies the "rgb_digital_aerial_photo_classifier.py" to digital aerial photo image chips and extracts out the estimated woody
FPC for the given area. This script was developted to assess the accuracy of Landsat satellite estimates of woody fpc. 

The five classes represent cover for;

Class               Pixel value            Description
------------------------------------------------------------------------------------------
Woody green:          1                    Green leaf for all woody vegetation 
Non-woody green:      2                    Green leaf from all non-woody vegetation
Bare/npv vegetation:  3                    Bare ground and senescent vegetation (woody and non-woody)
Shadow:               4                    Shadow
Branch/trunk:         5                    Branches and trunks of woody vegetation
------------------------------------------------------------------------------------------

The serielised pickle file is produced using: scikit-learn = 0.21.3

Details on the methodology to developt this classifier can be found in chapter 5:
Staben, G. (2020).Development of remote sensing products to investigate the impact of tropical cyclones on natural vegetation communities in the wet-dry tropics of northern Australia. Doctoral dissertation, University of Tasmania. 

Author: Grant Staben 
email: grant.staben@nt.gov.au
Date: 15/06/2020
Version: 1.0

###############################################################################################

MIT License

Copyright (c) 2020 Grant Staben

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

imglist : csv file 
            csv file containing the list of image chips to process.

direc : str
            is a string containing the directory path to the image chips - this is used to create the file path and name of the classified image chip.

csv : csv file
            name and directory path for the csv file containing the woody fpc estimates obtained from the image chips. 

"""

from __future__ import print_function, division

# import the requried modules
import sys
import os
import argparse
import pdb
import pandas as pd
import csv
import subprocess
import rasterio
import numpy as np


# command arguments 
def getCmdargs():

    p = argparse.ArgumentParser()

    p.add_argument("-s","--imglist", help="provide the path and name of the csv file with the list of imagery to process")
    
    p.add_argument("-d","--direc", help="path to the directory containing the imagery")
    
    p.add_argument("-c","--csv", help="provide the path to the directory and name of the csv file containing the results")
    
    cmdargs = p.parse_args()
    
    # if there is no image list the script will terminate
    if cmdargs.imglist is None:

        p.print_help()

        sys.exit()

    return cmdargs


def applyModel(imglist,directory):
    
    """
    produce the classified image from a image chip representing a site 
    and extract out the total fpc value for the plot. 
    Save the image chip and save out the fpc results as a csv file
    """
    site_list = []
    fpc_value_list = []
        
    # open the list of imagery and read it into memory
    df = pd.read_csv(imglist,header=None)
    
    for index, row in df.iterrows():
        rgb_image =  directory + (str(row[0]))
        
        fileN = (str(row[0]))
        
        outfile = directory + fileN[:-4] + '_rgb_comb_class.tif'
        
        #print (fileN)
        #print (outfile)         
 
        # call and run the vegetation index scripts
        # to get this to work on windows the code being called by os.system needs to be stored 
        # and run from the same directory. 
    
        cmd = "python rgb_digital_aerial_photo_classifier.py --reffile %s --outfile %s"% (rgb_image,outfile) 
        #subprocess.call(cmd, shell=True)    
        os.system(cmd)
        print (outfile + ' complete')
        
        # read in the classified image and calculate the estimated fpc
        # read in with rasterio
        dataset = rasterio.open(outfile)
        # read in the first band as numpy array
        band1 = dataset.read(1)
        
        # get the shape of the image chip which to calculate the percentage fpc
        numPixels = (band1.shape[0] * band1.shape[1])
        
        # get the number of pixels classifed as green mangroves and calculate the % FPC for the site 
        greenM = band1[band1 == 1]
        greenMc = (greenM.shape[0]) 
        fpc = (greenMc / numPixels)*100
        
        site_list.append(fileN)
        
        fpc_value_list.append(fpc)
        
    return (site_list, fpc_value_list)   
           
# calls in the command arguments and applyModel function.        
def mainRoutine():
    
    """
    main routine
    """
    
    cmdargs = getCmdargs()
    directory = str(cmdargs.direc)
    csvfile = str(cmdargs.csv)
    
    # call the function to classify and extract out the fpc estimates
    site_list, fpc_value_list = applyModel(cmdargs.imglist,directory)

    # save out the results to a csv file
    data = list(zip(site_list, fpc_value_list))
    
    results = pd.DataFrame(data,columns=['site','fpc'])
           
    results.to_csv(csvfile)
    
    
if __name__ == "__main__":
    mainRoutine()