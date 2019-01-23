# ground-truth-productions

This kit is a workshop for building data packages **at a given output resolution**, with scalings and tilings, ready for TensorFlow training from a ground truth data source.

The **models/eb_12_v07** directory contains working examples with sample results. 

This kit depends on **tensorflow**, **object_detection**, collections, contextlib2, copy, glob, io, json, lxml, math, numpy, os, pandas, PIL, random, time

This kit comprises:

1. A **data** directory containing one version of (minimal) ground truth data:<br>
    eb_12_v07
    
2. A **lib** directory containing Python modules.


3. A **models** directory containing working examples.

Everything happens in the **models** directory.

See the README.md file there for further details.


## Scalings
Given ground truth images at 1920x1080 and a desired output resolution of 480x270 then a sequence of scalings can be constructed.

![480x270@480x270](scaled_g_480x270@480x270_00-15-44_543-acd008-pi_1-(1).jpg)

![960x540@480x270](scaled_m_960x540@480x270_00-15-44_543-acd008-pi_1-(1).jpg)

![1600x900@480x270](scaled_s_1600x900@480x270_00-15-44_543-acd008-pi_1-(1).jpg)

![1920x1080@480x270](scaled_x_1920x1080@480x270_00-15-44_543-acd008-pi_1-(1).jpg)

## Tilings
Given ground truth images at 1920x1080 and a desired output resolution of 480x270 then a sequence of tiling permutations at various scales can be constructed.

Note that this uses randomly selected, unclassified, background images, and also unclassified tiles (e.g. see the sample ground truth).

![480x270@480x270](tiled_g_480x270@480x270_0_1-(2).jpg)

![960x540@480x270](tiled_m_960x540@480x270_0_1-(5).jpg)

![1600x900@480x270](tiled_s_1600x900@480x270_0_1-(6).jpg)

![1920x1080@480x270](tiled_x_1920x1080@480x270_0_1-(10).jpg)


