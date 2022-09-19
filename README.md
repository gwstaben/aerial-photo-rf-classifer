# **Digital Aerial Photograph Classifier (Random Forest)**
## Python scripts and jupyter notebooks to classify digital aerial photography using random forest. 

This code applies a random forest classifier to predict a number of cover classes from 8 bit digital aerial photography. The classifier
was trained on 15cm digital aerial photography captured across the topend of the Northern Territory between the years 2008 to 2018.

The aim of this classifier is to obtain estimates of woody green (woody Foliage projective cover) to validate satellite based models.

![alt text](https://github.com/gwstaben/aerial-photo-rf-classifer/blob/main/png/ap_class_example.PNG)

Example of 15cm Digital Aerial Photograph and the woody green vegetation class. 

The five classes represent cover for;

| Class |              Pixel value    |        Description |
|:----------------|:------------------|:-------------------|
| Woody green:      |   1          |          Green leaf for all woody vegetation |
| Non-woody green:  |   2          |         Green leaf from all non-woody vegetation |
| Bare/npv vegetation: | 3       |             Bare ground and senescent vegetation (woody and non-woody) |
| Shadow:          |    4       |            Shadow |
| Branch/trunk:     |   5       |            Branches and trunks of woody vegetation |

Details on the methodology to develop this classifier can be found in chapter 5:

Staben, G. (2020).Development of remote sensing products to investigate the impact of tropical cyclones on natural vegetation communities in the wet-dry tropics of northern Australia. Doctoral dissertation, University of Tasmania. https://eprints.utas.edu.au/37967/

