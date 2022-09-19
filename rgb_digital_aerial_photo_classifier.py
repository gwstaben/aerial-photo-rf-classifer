#!/usr/bin/env python

"""
This code applies a random forest classifer to predict a number of cover classes from 8 bit digital areial photogrpahy. The classifier
was trained on 15cm digital aerial photorgrpahy captured across the topend of the Northern Territory between the years 2008 to 2018. The five classes represent cover for;

Class               Pixel value            Description
------------------------------------------------------------------------------------------
Woody green:          1                    Green leaf for all woody vegetation 
Non-woody green:      2                    Green leaf from all non-woody vegetation
Bare/npv vegetation:  3                    Bare ground and senescent vegetation (woody and non-woody)
Shadow:               4                    Shadow
Branch/trunk:         5                    Branches and trunks of woody vegetation
------------------------------------------------------------------------------------------

The aim of this classifer is to obtain estimates of woody green (woody Foliage projective cover) to validate satellite based models. 

The serielised pickle file is produced using: scikit-learn = 0.21.3

Details on the methodology to developt this classifier can be found in chapter 5:
Staben, G. (2020).Development of remote sensing products to investigate the impact of tropical cyclones on natural vegetation communities in the wet-dry tropics of northern Australia. Doctoral dissertation, University of Tasmania. 

Author: Grant Staben 
email: grant.staben@nt.gov.au
Date 15/06/2020

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

reffile : raster image file .tif 
            is a string containing the directory path and the name of the input file.

outfile : raster image file .tiff
            is a string containing the name of the output directory path and classified file.

picklefile : serilised pickle file
            serilised random forest classifer using pickle library. The serilised pickle file is produced from the script aerial_photo_classifier_pickle_file.py.

"""

import sys
import os
import argparse
import pickle as pickle
import numpy as np
from rios import applier, fileinfo
import pdb
from sklearn.preprocessing import Imputer


def getCmdargs():
    """
    Get command line arguments
    """
    p = argparse.ArgumentParser()
    p.add_argument("--reffile", help="Input 8bit digital aerial photography")
    
    p.add_argument("--outfile", help="Name of output classified image")
    
    p.add_argument("--picklefile", default="rfc_cpickle_20200615.p",help="Input pickle file (default is %(default)s)")
    
    cmdargs = p.parse_args()
    
    if cmdargs.reffile is None:
        p.print_help()
        sys.exit()
        
    return cmdargs


def main():
    """
    Main routine
    
    """
    cmdargs = getCmdargs()
    controls = applier.ApplierControls()
    infiles = applier.FilenameAssociations()
    outfiles = applier.FilenameAssociations()
    otherargs = applier.OtherInputs()
    
    infiles.image = cmdargs.reffile
    
    imageExt = infiles.image
         
    controls.setReferenceImage(infiles.image) 
    
    outfiles.hgt = cmdargs.outfile
    
    otherargs.rf = pickle.load(open(cmdargs.picklefile, 'rb'))
    # no data value
    otherargs.refnull =  0

    applier.apply(doModel, infiles, outfiles, otherargs,controls=controls)

    
def doModel(info, inputs, outputs, otherargs):

    nonNullmask = (inputs.image[0] != otherargs.refnull)
    
    # get the shape of the annual image and convert it to the shape of a single band  
    imgshape = inputs.image.shape
    # convert the tuple to a list to convert all bands to represent 1 band and then convert it back to a tuple
    list_imgshape = list(imgshape)
    list_imgshape[0] = 1
    imgShape = tuple(list_imgshape)

    # read in the individual bands of the RGB imagery 
    red = (inputs.image[0][nonNullmask]).astype(np.float32)
    green = (inputs.image[1][nonNullmask]).astype(np.float32)
    blue = (inputs.image[2][nonNullmask]).astype(np.float32)
      
    # parse the variables into a np array and transform it to look like the pandas df 
    allVars= np.vstack([red,green,blue]).T
       
    # sets up the shape and dtype for the classified output  
    outputs.hgt = np.zeros(imgShape, dtype=np.uint8)
    
    # applies the rf classifer to produce the classified image
    if allVars.shape[0] > 0:
        # run check over the input data and replaces nan and infinity values
        allVars[np.isnan(allVars)] = 0.0
        allVars[np.isinf(allVars)] = 0.0
        
        hgt = otherargs.rf.predict(allVars)
        
        outputs.hgt[0][nonNullmask] = hgt

if __name__ == "__main__":
    main()
