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
res.build_data( 
    data_root = os.path.join( data_root, data_version ),
    data_version = data_version,
    model_version = model
) 
