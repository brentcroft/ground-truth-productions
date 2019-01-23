# ground-truth-productions

This kit is a workshop for building data packages **at a given output resolution**, with scalings and tilings, ready for TensorFlow training from a ground truth data source.

## Scalings
![1920x1080@720x405](scaled_x_1920x1080@720x405_09-41-20_391-acd008-pi_1-(1).jpg)

![1600x900@720x405](scaled_s_1600x900@720x405_09-41-20_391-acd008-pi_1-(1).jpg)

![960x540@720x405](scaled_m_960x540@720x405_09-41-20_391-acd008-pi_1-(1).jpg)

![720x405@720x405](scaled_g_720x405@720x405_09-41-20_391-acd008-pi_1-(1).jpg)

## Tilings
![1920x1080@720x405](tiled_x_1920x1080@720x405_0_1-(11).jpg)

![1600x900@720x405](tiled_s_1600x900@720x405_0_1-(7).jpg)

![960x540@720x405](tiled_m_960x540@720x405_0_1-(3).jpg)

![720x405@720x405](tiled_g_720x405@720x405_0_4-(2).jpg)




The **models/eb_12_v07** directory contains working examples with sample results. 


This kit depends on **tensorflow**, **object_detection**, collections, contextlib2, copy, glob, io, json, lxml, math, numpy, os, pandas, PIL, random, time



This kit comprises:

1. A **data** directory containing one version of ground truth data:<br>
    eb_12_v07
    
2. A **lib** directory containing Python modules.


3. A **models** directory containing working examples.

Everything happens in the **models** directory.

See the README.md file there for further details.
