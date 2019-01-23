
"""
    

"""
import os
import math
from copy import deepcopy
import json
import time

import numpy as np
import PIL
import pandas as pd

from lxml import etree
"""
    
    
"""
from object_detection.utils import visualization_utils as vis_util
"""

"""
current_milli_time = lambda: int(round(time.time() * 1000))
current_timestamp = lambda: time.strftime( "%Y-%m-%d %H:%M:%S", time.gmtime() )


    
def create_blank_images( dir=None, scales=[ 64, 128, 256, 512 ]):
    for d in scales:
        img = PIL.Image.new( 'RGB', ( d, d ), ( 255, 0, 0, 0 ) )
        img.save( os.path.join( dir, 'blank_{}x{}.gif'.format( d, d ) ), 'GIF', transparency=0 )    



"""
    Not strict JSON, so can receive from html script tags
"""    
def store_as_json( json_path=None, json_prefix=' = ', object={} ):
    json_text = json_prefix + json.dumps( object, sort_keys=True, separators=( ', ', ':' ), indent=4 )
    with open ( json_path, "w") as f:
        print( json_text, file=f )
        
    print( "Created new js file: {}".format( json_path ) ) 
"""


"""    
def load_from_json( json_path=None, json_prefix=' = ' ):
    if os.path.isfile( json_path ):
        with open( json_path, "r") as f:
            t = f.read()
            s = t.find( json_prefix )
            return json.loads( t[ s + len( json_prefix ):] )

    return None
"""


"""        
def update_dict_from_json( json_path=None, json_prefix='vis = ', updatee=None ):
    if updatee is None:
        updatee = {}
        
    if os.path.isfile( json_path ):
        try:
            with open( json_path, "r") as f:
                t = f.read()
                s = t.find( json_prefix )
                updatee.update( json.loads( t[ s + len( json_prefix ):] ) )
                
        except Exception as e:
            raise ValueError( "Failed to update from: {}".format( json_path ), e )

    return updatee   
"""


"""
def get_labeled_objects( classification_file=None, min_score_thresh=0, class_min_score_thresh=None ):
    labeled_objects = []
    tree = etree.parse( classification_file )
    root = tree.getroot()
    item = 0    
    for member in root.findall('object'):
        category_box = member.find( 'bndbox' )
        if category_box is None:
            continue
        class_name = member.find('name').text
        
        score = member.find('score')
        score = 100 if score is None else float( member.find('score').text )
        
        valid_score = ( score >= min_score_thresh )
        
        if class_min_score_thresh is not None and class_name in class_min_score_thresh:
            valid_score = ( score >= class_min_score_thresh[ class_name ] ) 
        if valid_score:        
            category_object = [ 
                class_name, 
                int(category_box[0].text), 
                int(category_box[1].text), 
                int(category_box[2].text), 
                int(category_box[3].text),
                score,
                item
            ]
            labeled_objects.append( category_object )
            item = item + 1
    return labeled_objects
"""


"""
def draw_objects_on_image( image = None, objects = None, class_colors = None, line_thickness = 5, no_scores=False ):
    # sort by score ([5]) so high score boxes overlay low scores
    objects.sort( key = lambda x: x[5])
    for box in objects:
        if box[0] in class_colors:
            class_color = class_colors[ box[0] ]
        else:
            print( "No class color for category: {}".format( box[0] ) )
            class_color = 'yellow'
            
        if no_scores:
            display_str_list=[ '{}'.format( box[0] ) ]
        else:
            display_str_list=[ '{} {}%'.format( box[0], str( round( box[5] * 100 ) ) ) ]
        
        # note unusual order of co-ords
        vis_util.draw_bounding_box_on_image(
            image, 
            box[2], 
            box[1], 
            box[4], 
            box[3],
            color=class_color, 
            thickness=line_thickness,
            display_str_list=display_str_list,
            use_normalized_coordinates=False 
        ) 
"""


"""        
def create_boxed_image( image_file=None, classification_file=None, save_file=None, image_box_details=None ):
    # unpack image_box_details
    min_score_thresh, class_min_score_thresh, class_colors, line_thickness, no_scores = image_box_details
    labeled_objects = get_labeled_objects( classification_file, min_score_thresh, class_min_score_thresh )  
    if len( labeled_objects ) > 0:
        image = PIL.Image.open( image_file, 'r' )    
        draw_objects_on_image( image, labeled_objects, class_colors, line_thickness, no_scores )
        image.save( save_file )
        return True
    else:
        return False
"""


"""
def path_leaf( path ):
    _, tail = os.path.split(path)
    return tail
"""


"""
def create_boxed_images( 
        classification_path=None, 
        image_path=None, 
        save_path=None, 
        prefix=None, 
        overwrite_images=False,
        min_score_thresh=0,
        class_min_score_thresh={}, 
        class_colors={}, 
        line_thickness=5,
        no_scores=False
    ):

    feature_files = [ 
        os.path.join( classification_path, x )
        for x in os.listdir( classification_path ) 
        if ( prefix is None or x.startswith( prefix ) ) and x.endswith( '.xml' )
    ]
    
    
    if not overwrite_images:
        try:
            existingImages = [ os.path.join( save_path, x ) for x in os.listdir( save_path ) if x.endswith( '.jpg' ) ]
            # rename to match xml
            existingImages = [ x.replace( '.jpg', '.xml' ) for x in existingImages ]
            
            print( 'No. existing boxed images: {}'.format( len( existingImages ) ) )
            
            feature_files = list( set( feature_files ) - set( existingImages ) )
        except:
            raise ValueError( 'Error subtracting existing boxed images [{}]: {}'.format( save_path + '*.jpg', sys.exc_info()[0] ) ) 

    num_files = len( feature_files )
    item = 0

    if num_files > 0:
        feature_files.sort()
        labeling_start_time = time.time()

        for ff in feature_files:

            filename = path_leaf( ff )
            
            image_file = os.path.splitext( filename )[ 0 ] + '.jpg';
            save_image_path = os.path.join( save_path, image_file )

            if not overwrite_images and os.path.isfile( save_image_path ):
                print( '  image [{}] already boxed'.format( save_image_path ) )
                continue 

            # might not create an image if scores are too low etc.
            # therefore only count ones that say they got created
            image_box_details = ( min_score_thresh, class_min_score_thresh, class_colors, line_thickness, no_scores )
            
            if create_boxed_image( 
                    image_file=os.path.join( image_path, image_file ), 
                    classification_file=ff, 
                    save_file=save_image_path,
                    image_box_details=image_box_details
                ):                
                item = item + 1
                if item % 50 == 0:
                    log_stats( "Boxed", labeling_start_time, item, num_files )

        # might not have labeled any
        if item > 0:
            labeling_end_time = time.time()
            labeling_duration = ( labeling_end_time - labeling_start_time )

            labeling_rate = 0
            labeling_s_per_i = 0
            if labeling_duration > 0:
                labeling_rate = round( item / labeling_duration, 3 )
                labeling_s_per_i = round( labeling_duration / item, 3 ) 

            print( 'Finished boxing {} images in {}s [{} s/i, {} i/s].'.format( num_files, round( labeling_duration, 2), labeling_s_per_i, labeling_rate ) )
        else:
            print( "No images were boxed." )
    else:
        print( "No classifications." )       
