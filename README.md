# **aerial-photo-rf-classifer**
## Python scripts and jupyter notebooks to classify digital aerial photography using random forest. 

This code applies a random forest classifer to predict a number of cover classes from 8 bit digital areial photogrpahy. The classifier
was trained on 15cm digital aerial photorgrpahy captured across the topend of the Northern Territory between the years 2008 to 2018. The five classes represent cover for;

| Class |              Pixel value    |        Description |
|:----------------|:------------------|:-------------------|
| Woody green:      |   1          |          Green leaf for all woody vegetation |
| Non-woody green:  |   2          |         Green leaf from all non-woody vegetation |
| Bare/npv vegetation: | 3       |             Bare ground and senescent vegetation (woody and non-woody) |
| Shadow:          |    4       |            Shadow |
| Branch/trunk:     |   5       |            Branches and trunks of woody vegetation |


The aim of this classifer is to obtain estimates of woody green (woody Foliage projective cover) to validate satellite based models.  

Details on the methodology to developt this classifier can be found in chapter 5:

Staben, G. (2020).Development of remote sensing products to investigate the impact of tropical cyclones on natural vegetation communities in the wet-dry tropics of northern Australia. Doctoral dissertation, University of Tasmania. https://eprints.utas.edu.au/37967/ 
