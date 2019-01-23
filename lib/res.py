"""

    Common library imports
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

    TensorFlow & Lucid imports
"""
import tensorflow as tf
import lucid.optvis.render as render

from lucid.misc.io.serialize_array import _normalize_array as normalize_array

import lucid.optvis.objectives as objectives
import lucid.optvis.param as param
import lucid.optvis.transform as transform
"""

    Local library imports
"""
from util import store_as_json
from util import load_from_json
from statty import xml_to_dataframe

import tfrecord as tfr
import production
import tiling
"""
    TODO:
    These two should be calculable from "statty.get_column_names()" + 1 for the index
"""
folder_index = 2
filename_index = 3
"""


""" 
def build_config( 
        local_root='.', 
        data_root=None, 
        data_version=None, 
        model_version=None
    ):

    if data_root is None:
        raise ValueError( "data_root cannot be None" )
        
    if data_version is None:
        raise ValueError( "data_version cannot be None" )   

    if model_version is None:
        raise ValueError( "model_version cannot be None" )    

    # 
    resolution_path = os.path.join( local_root, data_version, model_version )
     
    if not os.path.isdir( resolution_path ):
        os.makedirs( resolution_path )        

    
    res_path = os.path.join( resolution_path, "res.js" )
    
    if not os.path.isfile( res_path ):
    
        # create a default res file
        store_as_json( 
            json_path=res_path,
            json_prefix="res = ", 
            object={
            
            "abort": False,
            
            "data": data_version,
            "model": model_version,
            
            # the resolution at which product will be created
            "output_resolution": [ 320, 180 ],

            
            # these labels are excluded from "scaling" but used in "tiling"
            "background_classes": [ "unclassified" ],
          
            # production methods
            "product": {
                "parts": [ "eval", "train" ],
                "scaled": [
                   # prefix, sizes, area-ration-constraint
                   [ "g", [ 480, 270 ], 0.2 ],
                   [ "m", [ 960, 540 ], 0.2 ],
                   [ "s", [ 1600, 900 ], 0.2 ],
                   [ "x", [ 1920, 1080 ], 0.2 ]
                ],
                
                "tiled": [
                     {
                        'key': 'tight',
                        'crop': [ 100, 100 ],
                        'pad': 120,
                        'apertures': [
                            # prefix, sizes, area-ration-constraint, repeats
                            ( 's', [ 1440,  810 ], 0.2, 1 ),
                            ( 't', [ 1600,  900 ], 0.2, 1 ),
                            ( 'x', [ 1920, 1080 ], 0.2, 1 )
                        ]
                    }
                ]
            },
            
            # what training records to build - must match production parts
            "training_records": {
                "eval": {
                    "num_shards": 1,
                    "filename": "eval.record"
                },
                "train": {
                    "num_shards": 10,
                    "filename": "train.record"
                }
            }            
        } ) 
"""


""" 
def build_data_csv( 
        local_root='.', 
        data_root=None, 
        data_version=None, 
        model_version=None, 
        data_csv='data.csv'
    ):

    if data_root is None:
        raise ValueError( "data_root cannot be None" )
        
    if data_version is None:
        raise ValueError( "data_version cannot be None" ) 

    if model_version is None:
        raise ValueError( "model_version cannot be None" )        
        
    resolution_path = os.path.join( local_root, data_version, model_version )
    
    if not os.path.isdir( resolution_path ):    
        raise ValueError( "Invalid resolution path: {}".format( resolution_path ) )
    
    res_path = os.path.join( resolution_path, "res.js" )
    
    if not os.path.isfile( res_path ):    
        raise ValueError( "Invalid resolution file: {}".format( res_path ) )
    
    # check for existing file
    csv_path = os.path.join( resolution_path, data_csv )
    
    if not os.path.isfile( csv_path ):

        data_dirs = [
            os.path.join( data_root, dir )
            for dir in os.listdir( data_root )
            if not dir.startswith( "(" )
        ]
        
        data_frame = xml_to_dataframe( paths=data_dirs )
        
        # TODO:
        # check that every xml file matches a corresponding image file

        data_frame.to_csv( csv_path, index_label='index' )


        print( "Created data csv file: {}".format( csv_path ) )
    else:
        print( "Found data csv file: {}".format( csv_path ) )
        

    category_map_path = os.path.join( resolution_path, 'category_map.js' )
    
    if not os.path.isfile( category_map_path ):
    
        xsheet = pd.read_csv( csv_path, index_col='index' )
    
        category_labels = [ str( x ) for x in xsheet[ "class" ].unique() if x != 'unclassified' ]
        
        category_labels.sort()        
        
        category_map = {
            key: 1 + category_labels.index( key ) for key in sorted( category_labels )
        }
        
        store_as_json( json_path=category_map_path, json_prefix='cat = ', object=category_map )

        print( "Created category map: {}".format( category_map_path ) )    
    else:
        print( "Found category map file: {}".format( category_map_path ) )
"""

    Read the master data CSV, and rewrite data lines to two CSV files: train & eval.
    
    The splitting is done for each label class (to better control the presence of low quantity classes). 
    But, a single file may contain multiple boxes for different classes!
"""
def build_data_parts_csv( 
        local_root='.', 
        data_version=None, 
        model_version=None, 
        data_csv='data.csv', 
        train_csv='train.csv', 
        eval_csv='eval.csv', 
        group_by="class",
        max_eval_size=10,
        overwrite=False
        ):

    if data_version is None:
        raise ValueError( "data_version cannot be None" )  

    if model_version is None:
        raise ValueError( "model_version cannot be None" )          
        
    resolution_path = os.path.join( local_root, data_version, model_version )
    
    if not os.path.isdir( resolution_path ):    
        raise ValueError( "Invalid resolution path: {}".format( resolution_path ) )
    
    res_path = os.path.join( resolution_path, "res.js" )
    
    if not os.path.isfile( res_path ):    
        raise ValueError( "Invalid resolution file: {}".format( res_path ) )
    
    csv_path = os.path.join( resolution_path, data_csv )

    if not os.path.isfile( csv_path ):    
        raise ValueError( "Invalid data csv file: {}".format( csv_path ) )    
    
    
    train_csv_path = os.path.join( resolution_path, train_csv )
    eval_csv_path = os.path.join( resolution_path, eval_csv )

    if not overwrite and os.path.isfile( train_csv_path ) and os.path.isfile( eval_csv_path ): 
        print( "Found train csv file: {}".format( train_csv_path ) )
        print( "Found eval csv file: {}".format( eval_csv_path ) )
        return   
    
    
    xsheet = pd.read_csv( csv_path, index_col='index' )
    
    print( "Loaded data csv file: {}".format( data_csv ) )

    # capture any extra labels 
    extra_labels = xsheet[ xsheet['item'] > 1 ] 

    if len( extra_labels ) > 0:
        print( "Detected {} extra labels.".format( len( extra_labels ) ) )

    # drop any extra labels 
    file_labels = xsheet[ xsheet['item'] <= 1 ]

    # 
    group_train = []
    group_eval = []

    
    groups_container = ( file_labels.groupby( "edition" ) if group_by is None else file_labels.groupby( group_by ) )
    
    groups =  [ ( group_name, groups_container.get_group( group_name ) ) for group_name in groups_container.groups ]   
    
    
    
    # split each group into train and eval 
    for group_name, group in groups:
            
        group_indices = group.index

        num_items = len( group_indices )
        
        num_eval_items = min( max_eval_size, max( 1, int( num_items / 10 ) ) )
        
        # make a random pick of indices for this group's evaluation
        eval_indices = np.random.choice( group_indices, size=num_eval_items, replace=False )
            
        try:
            # the remainder are for training
            train_indices = [ i for i in group_indices if i not in eval_indices ]
                        
            for i in train_indices:
                try:
                    row = [ i ] + xsheet.iloc[ i ].values.tolist()
                    group_train.append( row )
                    
                except IndexError as e:
                    print( "IndexError: (train) {}; {}".format( i, e ) )            
            
            for i in eval_indices:
                try:
                    row = [ i ] + xsheet.iloc[ i ].values.tolist()
                    group_eval.append( row )
                    
                except IndexError as e:
                    print( "IndexError: (eval) {}; {}".format( i, e ) )                
            

            print( "Split group [{}]: train={}, test={}".format( group_name, len( train_indices ), len( eval_indices ) ) )

        except Exception as e:
            print( "Unexpected exception: {}".format( e ) )
            raise e


    if len( extra_labels ) > 0:
        
        num_in_train = 0
        num_in_eval = 0
        
        for i, row in extra_labels.iterrows():
        
            values = [ i ] + row.values.tolist()
            folder = values[ folder_index ]
            filename = values[ filename_index ]
            
            found_in_eval = [ 
                r 
                for r in group_eval 
                if r[ filename_index ] == filename and r[ folder_index ] == folder 
            ]
            
            if len( found_in_eval ) == 0:
                group_train.append( values )
                num_in_train = num_in_train + 1
            else:
                group_eval.append( values )  
                num_in_eval = num_in_eval + 1

        print( "Distributed extra labels: train={}, eval={}".format( num_in_train, num_in_eval ) )


    columns_labels = [ 'index' ] + xsheet.columns.values.tolist()
                
    train_df = pd.DataFrame.from_records( group_train, columns=columns_labels ).set_index( 'index' )
    eval_df = pd.DataFrame.from_records( group_eval, columns=columns_labels ).set_index( 'index' )        
                
                
    #
    train_df.to_csv( os.path.join( resolution_path, train_csv ), index_label='index' )
    print( "Saved train CSV: {}".format( train_csv ) )
    
    eval_df.to_csv( os.path.join( resolution_path, eval_csv ), index_label='index' )
    print( "Saved eval CSV: {}".format( eval_csv ) )
"""



"""
def build_data( 
        local_root='.',
        data_root=None,
        data_version=None, 
        model_version=None, 
        train_csv='train.csv', 
        eval_csv='eval.csv',
        progress_every=500,
        overwrite=False
        ):
        
    if data_root is None:
        raise ValueError( "data_root cannot be None" )
        
    if data_version is None:
        raise ValueError( "data_version cannot be None" )             

    if model_version is None:
        raise ValueError( "model_version cannot be None" )            
    
    resolution_path = os.path.join( local_root, data_version, model_version )
    
    if not os.path.isdir( resolution_path ):    
        raise ValueError( "Invalid resolution path: {}".format( resolution_path ) )
    
    res_path = os.path.join( resolution_path, "res.js" )
    
    if not os.path.isfile( res_path ):    
        raise ValueError( "Invalid resolution file: {}".format( res_path ) )
    
    res = load_from_json( json_path=res_path, json_prefix='res = ' )
    
    output_resolution = res[ 'output_resolution' ] if 'output_resolution' in res else None
    
    if output_resolution is None:
        raise ValueError( "No output_resolution in res file." )
    
    
    product = res[ 'product' ] if 'product' in res else None
    
    if product is None:
        raise ValueError( "No product in res file." )
      

    product_parts = product[ 'parts' ] if 'parts' in product else []
    product_scaled = product[ 'scaled' ] if 'scaled' in product else None
    product_tiled = product[ 'tiled' ] if 'tiled' in product else None
    
    parts_sheets = []
    
    if 'eval' in product_parts:
        eval_csv_path = os.path.join( resolution_path, eval_csv )
        if not os.path.isfile( eval_csv_path ) : 
            raise ValueError( "Missing eval csv file: {}".format( eval_csv_path ) )
            
        parts_sheets = parts_sheets + [ ( 'eval', pd.read_csv( eval_csv_path, index_col='index' ) ) ]
        print( "Loaded eval csv file: {}".format( eval_csv ) )      

    if 'train' in product_parts:
        train_csv_path = os.path.join( resolution_path, train_csv )
        if not os.path.isfile( train_csv_path ) : 
            raise ValueError( "Missing train csv file: {}".format( train_csv_path ) )

        parts_sheets = parts_sheets + [ ( 'train', pd.read_csv( train_csv_path, index_col='index' ) ) ]
        print( "Loaded train csv file: {}".format( train_csv ) )    
    
    
    
    
    background_classes = res['background_classes'] if 'background_classes' in res else None
    
    # in this case we rely on this directory only containing images with no significant categories
    background_image_generator = production.get_background_image_generator(
        background_dir = os.path.join( data_root, 'unclassified' )
    )
                    
    
    if product_scaled is not None:
        print( "Generating scaled products..." ) 
        
        for scaling in product_scaled:
            prefix = scaling[0]
            container_size = scaling[1]
            area_ratio = scaling[2]
            
            for part, xsheet in parts_sheets:
            
                output_path = os.path.join( resolution_path, part, 'scaled' )

                tile_prefix = 'scaled_{}_{}x{}@{}x{}'.format( prefix, container_size[0], container_size[1], output_resolution[0], output_resolution[1] )
            
                if os.path.isdir( output_path ):
                    num_existing = len( [ f for f in os.listdir( output_path ) if f.startswith( tile_prefix ) and f.endswith( '.xml' ) ] )
                    if num_existing > 0:
                        if overwrite:
                            print( "    [{}] clearing [{}] {} entries.".format( part, tile_prefix, num_existing ) )                        
                            for f in [ f for f in os.listdir( output_path ) if f.startswith( tile_prefix ) ]:
                                os.remove( os.path.join( output_path, f ) )
                        else:
                            print( "    [{}] skipping [{}] {} entries.".format( part, tile_prefix, num_existing ) )
                            continue  
                
            
                print( "  building scaled product part: {}/{}*".format( part, tile_prefix ) )
                
                num_items = len( xsheet )
                num_checked = 0
                count = 0   
                
                for i, row in xsheet.iterrows():
                
                    values = [ i ] + row.values.tolist()
                    folder = values[ folder_index ]            

                    image_filename = values[ filename_index ]
                    meta_filename = image_filename.replace( ".jpg", ".xml" )

                    image_tiles = tiling.get_image_tiles( 
                            meta_path = os.path.join( data_root, folder, meta_filename ), 
                            crop_scale = container_size, 
                            padder = None, 
                            no_meta = background_classes,
                            constraint = lambda box: production.area_within_limit( box, container_size, ratio=area_ratio )
                        )

                    num_checked = num_checked + 1
                        
                    if len( image_tiles ) > 0:
                        num_tiles_created = tiling.export_tiles(
                            tiles = image_tiles,
                            seq = image_filename.split(".")[0],                            
                            tile_prefix = tile_prefix,
                            no_meta = background_classes, 
                            container_size = container_size,
                            output_size = output_resolution,
                            output_path = output_path
                        )
                        if num_tiles_created > 0:
                            count = count + 1
                        
                    if num_checked % progress_every == 0:
                        print( "    [{}] scaled products examined: {}/{}".format( part, num_checked, num_items ) )

                        
                print( "    [{}] scaled products exported: {}/{}".format( part, count, num_items ) ) 
                
                    
                    
                    
    if product_tiled is not None:
        for tiling_details in product_tiled:
            
            crop_scale = tiling_details['crop']
            key = tiling_details['key']
            pad = tiling_details['pad']
            
            apertures = tiling_details['apertures']
            
            print( "Generating tiled product: {}".format( key ) )
            
            for part, xsheet in parts_sheets:
            
                tiles = []
            
                output_path = os.path.join( resolution_path, part, 'tiled' )

                print( "  building tiles: {} crop={}".format( part, crop_scale ) )
                
                num_items = len( xsheet )
                
                for i, row in xsheet.iterrows():
                
                    values = [ i ] + row.values.tolist()
                    folder = values[ folder_index ]            

                    image_filename = values[ filename_index ]
                    meta_filename = image_filename.replace( ".jpg", ".xml" )

                    # including unclassified
                    image_tiles = tiling.get_image_tiles( 
                            meta_path = os.path.join( data_root, folder, meta_filename ), 
                            crop_scale = crop_scale, 
                            padder = lambda size: pad
                        )
                        
                    tiles.extend( image_tiles )


                print( "  obtained tiles: {} crop={}, num_tiles={}".format( part, crop_scale, len( tiles ) ) )

                    
                for aperture in apertures:
                    prefix = aperture[0]
                    container_size = aperture[1]
                    area_ratio = aperture[2]
                    repeats = aperture[3]

                    tile_prefix = 'tiled_{}_{}x{}@{}x{}'.format( 
                        prefix,
                        container_size[0], 
                        container_size[1], 
                        output_resolution[0], 
                        output_resolution[1]
                    )
                
                
                    if os.path.isdir( output_path ):
                        num_existing = len( [ f for f in os.listdir( output_path ) if f.startswith( tile_prefix ) and f.endswith( '.xml' ) ] )
                        if num_existing > 0:
                            if overwrite:
                                print( "    [{}] removing from [{}] {} entries.".format( part, tile_prefix, num_existing ) )
                                for f in [ f for f in os.listdir( output_path ) if f.startswith( tile_prefix ) ]:
                                    os.remove( os.path.join( output_path, f ) )
                            else:
                                print( "    [{}] skipping [{}] {} entries.".format( part, tile_prefix, num_existing ) )
                                continue   


                    
                    for i in range( repeats ):
                        num_tiles_created = tiling.export_tiles(
                            tiles = tiles,
                            seq = i,
                            tile_prefix = tile_prefix,
                            no_meta = background_classes, 
                            container_size = container_size,
                            tile_margin=(0,0,0,0),
                            image_acceptor_factors=(0,0,0,0),                        
                            output_size = output_resolution,
                            output_path = output_path,
                            background_image_generator=background_image_generator,
                            constraint = lambda box: production.area_within_limit( box, container_size, ratio=area_ratio )
                        )

                        print( "    [{}] tiled products exported: {}_{}={}".format( part, tile_prefix, i, num_tiles_created ) )                         
                
                tiles = None
"""


"""                
def build_training_records( 
        local_root='.',
        data_version=None, 
        model_version=None
    ):
        
        
    if data_version is None:
        raise ValueError( "data_version cannot be None" )             

    if model_version is None:
        raise ValueError( "model_version cannot be None" )   
        
    resolution_path = os.path.join( local_root, data_version, model_version )
    
    if not os.path.isdir( resolution_path ):    
        raise ValueError( "Invalid resolution path: {}".format( resolution_path ) )
    
    res_path = os.path.join( resolution_path, "res.js" )
    
    if not os.path.isfile( res_path ):    
        raise ValueError( "Invalid resolution file: {}".format( res_path ) )
    
    res = load_from_json( json_path=res_path, json_prefix='res = ' )        
        
    training_records = res['training_records'] if 'training_records' in res else None
    
    if training_records is None:
        raise ValueError( "missing 'training_records' from resolution file: {}".format( res_path ) )

        
    category_map_path = os.path.join( resolution_path, 'category_map.js' )
    
    if not os.path.isfile( category_map_path ):
        raise ValueError( "Invalid class protobuf file: {}".format( category_map_path ) )
        
    category_map = load_from_json( json_path=category_map_path, json_prefix='cat = ' )
    
    
    
    product = res[ 'product' ] if 'product' in res else None
    
    if product is None:
        raise ValueError( "No product in res file." )    
    
    
    
    
    part_records = [ 
        ( k, v['filename'] if 'filename' in v else "{}.record".format( k ), v['num_shards'] if 'num_shards' in v else 1 ) 
        for k, v in training_records.items() 
    ]
    
    for part, record, shards in part_records:
    
        image_root = os.path.join( resolution_path, part )
        
        dirs = [ d
            for d in [ 
                os.path.join( image_root, k ) for k in product 
            ]
            if os.path.isdir( d )
        ]

        print( "Reading directories: {}".format( dirs ) )
        
        xsheet = xml_to_dataframe( dirs )

        if len( xsheet ) == 0:
            print( "No data found in part: {}".format( part ) )
            continue
        
        # save the datasheet in the part directory
        xsheet.to_csv( os.path.join( image_root, 'data.csv' ) )
        
        tfr.processCsvFileShards( 
            xsheet = xsheet, 
            image_root = image_root,
            output_path = os.path.join( resolution_path, '{}.record'.format( part ) ), 
            category_numbers = category_map,
            num_shards = shards
        )
        
        print( "Created {} records: shards={}".format( part, shards ) )      
