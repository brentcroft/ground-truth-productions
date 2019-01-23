"""
"""
import os
import sys
sys.path.append("../lib")

import res
import properties
PROPS = properties.Properties( "config.properties" )

data_root = PROPS["DATA"]
data_version = PROPS["DATA_VERSION"]
model = PROPS["MODEL"]
"""


"""
res.build_training_records( 
    data_version = data_version,
    model_version = model
) 