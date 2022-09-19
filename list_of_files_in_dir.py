# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:41:41 2016

@author: grants
"""

import fnmatch
import os
import argparse
import sys
import csv


def getCmdargs():
    """
    Command line arguments to indentify the directory and the file extentin to create a list for
    """
    p = argparse.ArgumentParser()

    p.add_argument("--direc", help="path to directory to look in")
    
    p.add_argument("--exten", help="extention to search for e.g. .csv")
    
    p.add_argument("--txtfile", help="name of out put txt file containing the list of files")
    
    
    cmdargs = p.parse_args()
    
    if cmdargs.exten is None:

        p.print_help()

        sys.exit()

    return cmdargs
    


def listdir(dirname, pattern="*"):
    """
    this function will return a list of files in a directory for the given file extention. 
    """
    return fnmatch.filter(os.listdir(dirname), pattern)

   
def mainRoutine():
    
    cmdargs = getCmdargs() # instantiate the get command line function
    
    direc = cmdargs.direc 
    exten = '*' + cmdargs.exten
 
    filelist = listdir(direc, exten)

    txtname = cmdargs.txtfile  
    
    # assumes that filelist is a flat list, it adds a  
    with open(txtname, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for file in filelist:
            writer.writerow([file])
      	

if __name__ == "__main__":
    mainRoutine()

