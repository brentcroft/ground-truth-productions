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
    
def load_from_json( json_path=None, json_prefix=' = ' ):
    if os.path.isfile( json_path ):
        with open( json_path, "r") as f:
            t = f.read()
            s = t.find( json_prefix )
            return json.loads( t[ s + len( json_prefix ):] )

    return None
    
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
    
    
    
    
    