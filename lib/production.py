"""

    Common library imports
"""
import os
import glob
import random
from PIL import Image
"""

    Local library imports
"""
import ground_truth as GT
import tiling
"""


"""
def area_within_limit( box, aperture, ratio=0.25 ):
    return GT.rect_area( box ) < ( ratio * aperture[0] * aperture[1] )
"""


    Provides an image generator that makes a random pick of a JPEG from a given directory.
    
    Assumes that "background_dir" contains JPEGs with no significant labelled boxes.
"""   
def get_background_image_generator( background_dir = None ):
    background_images = [ 
        os.path.basename( c )
        for c in [ s for s in glob.glob( os.path.join( background_dir, "*.jpg" ) ) ] 
    ]

    # provide a background image genarator
    def background_image_generator():
        jpg_path = os.path.join( background_dir, random.choice( background_images ) )
        with open(jpg_path, 'rb') as f:
            img = Image.open(f)
            img.load()     
        return img
    return background_image_generator
"""

    TODO: not used, remove
"""
def export_raw_tiling( image_path=None, meta_path=None, no_meta=None, output_resolution=None, output_path=None ):
             
    # load the meta
    image_meta = GT.get_file_meta( meta_path )
    
    # get boxes (excluding no_meta)
    boxes = [ 
        [ 
            mo["name"],
            mo["box"][0],
            mo["box"][1],
            mo["box"][2],
            mo["box"][3]
        ] 
        for mo in image_meta["objects"]
        if no_meta is None or mo["name"] not in no_meta
    ]           
    
    if len( boxes ) > 0:

        classification_image = Image.open( image_path )
        classification_image.load()

        tile = [ classification_image, boxes, [ meta_path ] ]

        tiling.write_tile( 
            tile=tile, 
            tile_id=image_meta["filename"], 
            tile_prefix="raw", 
            output_resolution=output_resolution, 
            output_path=output_path 
        )
            
        classification_image.close()
