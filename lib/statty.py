"""

    Common library imports
"""
import os
import glob
import pandas as pd
import numpy
import random
"""

    Local library imports
"""
import ground_truth as GT
"""

    Local constants
"""
IMAGE_ATTRIBUTE_COLUMNS = {
    "quality": "image_quality",
    "untruth-count": "untruth-count"
}
OBJECT_ATTRIBUTE_COLUMNS = {
    "aspect": "aspect", 
    "quality": "object_quality",
    "box-score": "box-score",
    "class-error": "class-error",
    "class-error-score": "class-error-score"
}
"""



"""
def get_column_names():
    column_names = [ 'edition', 'folder', 'filename', 'width', 'height' ]
    for attr_name in IMAGE_ATTRIBUTE_COLUMNS:
        column_names += [ attr_name ]
    column_names += [ 'item', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'score' ]
    for attr_name in OBJECT_ATTRIBUTE_COLUMNS:
        column_names += [ attr_name ]
    return column_names
"""



"""
def get_attributes_values( columns_dict, attributes ):
    values = []
    for attr_name in columns_dict:
        if attributes is None:
            values += [ None ]
        else:
            if attr_name in attributes:
                values += [ attributes[attr_name] ]
            else:
                values += [ None ]
    return values
"""


    Build a list of box details to be loaded as a dataframe.
"""
def load_classifications( paths=None, edition = "_" ):
    classifications = []
    for path in paths:
        
        # record the folder the file was found in
        folder = os.path.basename( path )
        
        for xml_file in glob.glob( path + '/*.xml' ):
            
            gt_meta = GT.get_file_meta(xml_file)

            width, height, depth = gt_meta['size']

            image_values = [ edition, folder, gt_meta["filename"], width, height ]

            image_attributes = gt_meta["attributes"]

            for attr_name in IMAGE_ATTRIBUTE_COLUMNS:
                if image_attributes is None:
                    image_values += [ None ]
                else:
                    if attr_name in image_attributes:
                        image_values += [ image_attributes[ attr_name ] ]
                    else:
                        image_values += [ None ]

            item_no = 0

            if "objects" in gt_meta:
                for member in gt_meta["objects"]:

                    item_no = item_no + 1
                    
                    object_values = []

                    if "box" in member:
                        bb = member["box"]

                        if bb is not None:
                            object_values += [
                                item_no,
                                member["name"],
                                bb[0],
                                bb[1],
                                bb[2],
                                bb[3],
                                member["score"]
                            ]
                            
                    if "attributes" in member:                        
                        object_values += get_attributes_values( OBJECT_ATTRIBUTE_COLUMNS, member["attributes"] )

                    classifications.append( image_values + object_values )

    print( "Loaded distinct items: {}".format( len( classifications ) ) )
    
    return classifications
"""



"""
def xml_to_dataframe( paths = None, edition = "_" ):
    if paths is None:
        raise ValueError( "paths cannot be null" )
        
    return pd.DataFrame( 
        load_classifications( 
            paths = paths, 
            edition = edition 
        ), 
        columns=get_column_names()
    )
