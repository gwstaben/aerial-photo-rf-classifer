#!/usr/bin/env python

"""
This code trains the random forest classifer to predict a number of cover classes from 8 bit digital areial photogrpahy. The classifier
was trained on digital aerial photorgrpahy captured across the topend of the Northern Territory between the years 2008 to 2018. The five 
classes represent cover for;

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

The script named: "rgb_digital_aerial_photo_classifier.py" applies the classifier to the input aerial photography.

Details on the methodology to developt this classifier can be found in chapter 5:
Staben, G. (2020).Development of remote sensing products to investigate the impact of tropical cyclones on natural vegetation communities in the wet-dry tropics of northern Australia. Doctoral dissertation, University of Tasmania. 

Author: Grant Staben 
email: grant.staben@nt.gov.au
Date 14/06/2020

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


"""
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt
import pandas as pd
import numpy as np
from random import sample
import matplotlib.pyplot as plt
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import pickle
from sklearn.metrics import confusion_matrix
pd.options.mode.chained_assignment = None  # default='warn'
plt.rcParams['figure.figsize'] = (2, 2)


def main():
    
    # read in the csv file containing the training data, which should be stored with this script.   
    df = pd.read_csv('comb_rgb_training_data_n17012.csv', header=0)
    
    # check all the classes are present
    print(df['class'].unique())
    
    train = df[['class', 'b1', 'b2', 'b3']] 

    class_names = train['class'].unique()
    
    # select out the predictor variables    
    tr = train[['b1', 'b2', 'b3']]

    # select out the class variables
    target1 = train[['class']]
    tar = target1.values
    target = tar.ravel()
    
    # cross validation data randomly selected
    
    X_train, X_test, y_train, y_test = train_test_split(tr, target, test_size=0.20, random_state=20)
    print ('this is the size of the training data ', X_train.shape, y_train.shape)
    print  ('this is the size of the testing data ',X_test.shape, y_test.shape)
    #print tr1.shape
    
    
    #create and train the random forest
    rf = RandomForestClassifier(n_estimators=200, n_jobs=-1)
    rfc = rf.fit(X_train, y_train)
    results = rfc.predict(X_test)
   
    
    # feature importance calculations
    feature_importance = rf.feature_importances_
    fi = enumerate(rf.feature_importances_)    
    cols = tr.columns 
    fiResult = [(value,cols[i]) for (i,value) in fi]
    fiResult = np.array(fiResult)
    score = np.float64(fiResult[:,0])
    band = fiResult[:,1]
    a = fiResult[np.argsort(fiResult[:, 1])]

    df = pd.DataFrame(dict(band=band,n=score))
    dfsort = df.sort_values(['n'], ascending=[False])


    # my complicated way to get the bar plot to sort in ascending order and display the assocated band names in the y axis 

    dfsort2 = df.sort_values(['n'], ascending=[True])
    b = dfsort2[['band']]
    c = b.values.tolist()
    # convert the list of band names in the correct order to a string
    e = str(c)
    # strips all the rubbish from the string 
    f = e.replace('[','').replace(']','').replace("'",'').replace(",",' ')
    # convert the cleaned up string back into a list to plot the band names in the bar graph
    g = f.split()

    ind = np.arange(len(df))
    width = 0.4

    fig, ax = plt.subplots()
    ax.barh(ind, dfsort2.n, width, color='blue')
    ax.set(yticks=ind + width, yticklabels= g, ylim=[2*width - 1, len(df)])
    plt.show()
    fig.savefig('Band_importance_score_aerial_photo_classifer.pdf',dpi=100)
 
    
    r2 = rf.score(X_test, y_test, sample_weight=None)
    print ('Overall accuracy of the classifier =',r2)
    y_test_predict = rf.predict(X_test)
    #plt.scatter(y_test_predict, y_test)
    cmap=plt.cm.Blues
    m = confusion_matrix(y_test, y_test_predict)
    plt.matshow(m, cmap=cmap)
    plt.colorbar()
    
    #out_results = [results, y_2]
    df_p = pd.DataFrame(results)
    df_o = pd.DataFrame(y_test)
    df_r = pd.concat([df_p, df_o], axis=1)
    #print (df_r)
    df_r.to_csv('test_results_for_AerialPhoto_classifer_errorMatrix.csv')
    
    """uncomment the code below and change the cpickle file name to save out the random forest classifer"""
   
    # save out model to a cPickle file 
    with open('rfc_cpickle_20200615.p', 'wb') as f:
        pickle.dump(rfc, f,protocol=2)

if __name__=="__main__":
    main()