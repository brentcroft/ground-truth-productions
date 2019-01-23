"""

    Common library imports
"""
import copy
import glob
import os
import random
from PIL import Image
"""

    Local library imports
"""
import ground_truth as GT
"""
"""
def get_tail( path, tail=0 ):
    x = os.path.split( path )
    if tail > 0 and len( x ) > 1:
        return os.path.join( get_tail( x[0], tail - 1 ), x[-1] )
    return x[-1]
"""

    centre crop with boundary correction
"""
def get_crop_coords( boundingBox, width, height, maxW, maxH, padder=None ):
    
    # crop to same dimensions
    if width == maxW and height == maxH:
        return [ 0, 0, width, height ]
    
    # box size
    bw, bh = ( boundingBox[ 2 ] - boundingBox[ 0 ] ), ( boundingBox[ 3 ] - boundingBox[ 1 ] )
    
    if padder is None:
        pad = 20
    else:
        pad = padder( ( bw, bh ) )
    
    # centre coords
    cx, cy = boundingBox[ 0 ] + bw / 2, boundingBox[ 1 ] + bh / 2

    # crop coords at centre
    cx1, cy1, cx2, cy2 = cx - ( maxW / 2 ), cy - ( maxH / 2 ), cx + ( maxW / 2 ), cy + ( maxH / 2 )
    
    # pad
    cx1 -= pad
    cy1 += pad
    cx2 -= pad
    cy2 += pad
    
    # adjust within extents
    if cx1 < 0:
        # i.e. cx1 is negative
        cx2 = cx2 - cx1
        cx1 = 0

    if cx2 > width:
        cx1 = cx1 - ( cx2 - width )
        cx2 = width
        
    if cy1 < 0:
        # i.e. cy1 is negative
        cy2 = cy2 - cy1
        cy1 = 0
        
    if cy2 > height:
        cy1 = cy1 - ( cy2 - height )
        cy2 = height


    if cx1 > boundingBox[ 0 ]:
        cx1 = max( boundingBox[ 0 ] - pad, 0 )

    if cx2 < boundingBox[ 2 ]:
        cx2 = min( boundingBox[ 2 ] + pad, width )
        
    if cy1 > boundingBox[ 1 ]:
        cy1 = max( boundingBox[ 1 ] - pad, 0 )
        
    if cy2 < boundingBox[ 3 ]:
        cy2 = min( boundingBox[ 3 ] + pad, height )
        
    return [ int(cx1), int(cy1), int(cx2), int(cy2) ]
"""


"""
def get_min_max( members=None, source_scale=None, crop_scale=None, padder=None ):
    width, height = source_scale
    CROP_WIDTH, CROP_HEIGHT, TARGET_WIDTH, TARGET_HEIGHT = crop_scale    
    min_max_coords = [ width, height, 0, 0 ]

    if len( members ) > 0:
        for member in members:
            box = member[1]
            boxBounds = [ box[0], box[1], box[2], box[3] ]

            min_max_coords = [
                min( min_max_coords[0], boxBounds[0] ),
                min( min_max_coords[1], boxBounds[1] ),
                max( min_max_coords[2], boxBounds[2] ),
                max( min_max_coords[3], boxBounds[3] )
            ]
    cropCoords = get_crop_coords( min_max_coords, width, height, CROP_WIDTH, CROP_HEIGHT, padder=padder ) 
"""


"""
def translate_box( box=None, crop_coords=(0,0) ):
    xoff = crop_coords[0]
    yoff = crop_coords[1]

    return [
        box[0] - xoff,
        box[1] - yoff,
        box[2] - xoff,
        box[3] - yoff
    ] 
"""


"""
def get_scale_ratios( crop_scale ):
    return [ 
        ( float( crop_scale[2] ) / crop_scale[0] ), 
        ( float( crop_scale[3] ) / crop_scale[1] ) 
    ]
"""


"""
def scale_box( box=None, input_resolution=None, output_resolution=None ):
    # scale meta data                
    xr, yr = get_scale_ratios( [
        input_resolution[0], 
        input_resolution[1],
        output_resolution[0], 
        output_resolution[1]
    ] )
    try:
        return (
            int( round( xr * box[0] ) ), 
            int( round( yr * box[1] ) ),
            int( round( xr * box[2] ) ), 
            int( round( yr * box[3] ) )
        )
    except Exception as e:
        raise ValueError( "xr=[{}], yr=[{}], box=[{}], input_resolution=[{}], output_resolution=[{}]".format( xr, yr, box, input_resolution, output_resolution ) )
"""


"""
def overlap( A, B ):
    XA1, YA1, XA2, YA2 = A
    XB1, YB1, XB2, YB2 = B
    return ( min(XA2, XB2) - max(XA1, XB1) ), ( min(YA2, YB2) - max(YA1, YB1) )
"""


"""       
def remove_overlappers( source_scale=None, crop_scale=None, members=None, max_overlap=-10, source=None, no_meta=None, padder=None ):

    width, height, _ = source_scale
    CROP_WIDTH, CROP_HEIGHT = crop_scale

    # remove  members that occlude each other
    # use dummy call to padder
    overlappers = []
    for i in range( 0, len( members ) ):
        memberI = members[i]
        if no_meta is not None and memberI["name"] in no_meta:
            continue

        boxICropCoords = get_crop_coords( memberI["box"], width, height, CROP_WIDTH, CROP_HEIGHT, padder=padder )                  

        for j in range( i + 1, len( members ) ):
            memberJ = members[j]
            if no_meta is not None and memberJ["name"] in no_meta:
                continue

            boxJCropCoords = get_crop_coords( memberJ["box"], width, height, CROP_WIDTH, CROP_HEIGHT, padder=padder )                  
            ox, oy = overlap( boxICropCoords, boxJCropCoords )
            
            if min( ox, oy ) > max_overlap:
                # we don't want either
                if memberI not in overlappers:
                    overlappers.append( memberI ) 
                if memberJ not in overlappers:
                    overlappers.append( memberJ ) 

    if overlappers:
        members = [ m for m in members if m not in overlappers ]

    return members  
"""


"""
def get_image_tiles( meta_path=None, crop_scale=(100,100), padder=None, no_meta=None, constraint=None ):
    
    image_meta = GT.get_file_meta( meta_path )
    
    source_scale = image_meta["size"]
    
    meta_objects = remove_overlappers(
        source_scale=source_scale,
        crop_scale=crop_scale,
        members = image_meta["objects"], 
        max_overlap=-10, 
        source=meta_path 
    )

    if len( meta_objects ) < 1:
        return []
    
    jpg_path = meta_path.replace( ".xml", ".jpg" )

    width, height, _ = source_scale
    CROP_WIDTH, CROP_HEIGHT = crop_scale
    
    source = get_tail( meta_path, 2 )

    tiles = []

    for member in meta_objects:

        label = member["name"]
        
        if no_meta is not None and label in no_meta:
            continue
        
        box = member["box"]
        
        if constraint is not None and not constraint( box ):
            continue        

        cropCoords = get_crop_coords( box, width, height, CROP_WIDTH, CROP_HEIGHT, padder=padder  )  
        crop_size = ( cropCoords[2] - cropCoords[0], cropCoords[3] - cropCoords[1] )

        # see: https://github.com/python-pillow/Pillow/issues/2019
        # We need to consume the whole file inside the `with` statement
        with open(jpg_path, 'rb') as f:
            image = Image.open(f)
            image.load()        
        
        cropped_image = image.crop( cropCoords )
        
        bb1 = translate_box( crop_coords=cropCoords, box=box )

        tiles.append( [ 
            cropped_image, 
            [ [ label, bb1[0], bb1[1], bb1[2], bb1[3] ] ], 
            [ str( source ) ],
            source_scale,
            crop_scale
        ] )
    
    return tiles     
"""


"""
def get_tiles( classification_folder, crop_scale=None, padder=None, no_meta=None, constraint=None, exporter=None, exportMode=None ):
    tiles = []
    for xml_file in glob.glob( os.path.join( classification_folder, '*.xml' ) ):
        image_tiles = get_image_tiles( 
                xml_file, 
                crop_scale=crop_scale, 
                padder=padder, 
                no_meta=no_meta,
                constraint=constraint
            ) 
        if len( image_tiles ) > 0:
            
            if exporter is not None:
                exporter( image_tiles, exportMode )
            else:
                tiles.extend( image_tiles )
                
            
    return tiles
"""


"""
def write_tile( tile=None, tile_id=None, tile_prefix="tile", output_resolution=None, output_path=None ):

    if output_path is None:
        raise ValueError("output_path is None")
            
    image, meta, sources = tile

    new_objects_meta = [ [ i for i in m ] for m in meta ] 

    tile_sig = '{}_{}-({})'.format( tile_prefix, tile_id, len( new_objects_meta ) )

    
    # maybe shrink image and meta resolution from input to output
    if output_resolution is not None:
        input_resolution = image.size
        image = image.resize( output_resolution, Image.ANTIALIAS  ) 
        for nom in new_objects_meta:
            nom[1], nom[2], nom[3], nom[4] = scale_box( 
                ( nom[1], nom[2], nom[3], nom[4] ), 
                input_resolution, 
                output_resolution 
            )
            
        # dumb check - can remove??
        for nom in new_objects_meta:
            if nom[3] < nom[1]:
                x = nom[1];
                nom[1] = nom[3]
                nom[3] = x
                print( "Bad box: swapped x1, x2: [{}]".format( tile_sig ) )
            if nom[4] < nom[2]:
                x = nom[2];
                nom[2] = nom[4]
                nom[4] = x
                print( "Bad box: swapped y1, y2: [{}]".format( tile_sig ) )
    else:
        output_resolution = input_resolution


    image_file = "{}.jpg".format( tile_sig )
    meta_file = "{}.xml".format( tile_sig )
    
    if not os.path.exists( output_path ):
        os.makedirs( output_path )    

    image.save( os.path.join( output_path, image_file ) )

    new_meta = {
        "filename": image_file,
        "size": ( output_resolution[0], output_resolution[1], 3 ),
        "attributes": {
            "sources": str( sources )
        }
    }  
    
    new_meta["objects"] = [
        {
            "name": nom[0], 
            "box": ( nom[1], nom[2], nom[3], nom[4] )
        }
        for nom in new_objects_meta
    ]
    
    GT.put_file_meta( os.path.join( output_path, meta_file ), new_meta )
"""

    recursive tiling
"""
def fill_tile( 
        container_size=None, 
        offset=None, 
        items=None, 
        tile=None, 
        tile_meta=None, 
        tile_sources=None, 
        tile_margin=None,
        no_meta=None, 
        orientation=None, 
        flips=None,
        allow_diagonal=True,
        auto_orient=True
    ):
    
    if len( items ) < 1:
        return 0;
    
    width, height = container_size
    
    if tile_margin is None:
        tile_margin = (0,0,0,0)
        
    tile_margin_width = tile_margin[0] + tile_margin[2]
    tile_margin_height = tile_margin[1] + tile_margin[3]  
    
    candidates = [ 
        item 
        for item in items 
        if ( tile_margin_width + item[0].size[0] ) <= width and ( tile_margin_height + item[0].size[1] ) <= height
    ]
    
    if not candidates:
        # is the image too big
        if offset[0]==0 and offset[1]==0:
            # no more images that will fit!
            return 0

        return 0

    
    candidate = random.choice( candidates )

    image, meta, sources, _, _ = candidate
    
    image_width = image.size[0] + tile_margin_width
    image_height = image.size[1] + tile_margin_height
    
    #
    items.remove( candidate )
    
    # new instance of meta
    meta = [ 
        m[0:5]
        for m in meta 
        if no_meta is None or m[0] not in no_meta
    ]

    # extend sources
    if tile_sources is not None:
        tile_sources.extend( sources ) 

    # maybe flips
    if flips is not None:
        if len( flips ) > 0 and random.randint( 0, flips[0] ) == 0:
            image = image.transpose( Image.FLIP_LEFT_RIGHT )
            for m in meta:
                m1, m3 = m[1], m[3]
                m[3] = image.size[0] - m1
                m[1] = image.size[0] - m3

        if len( flips ) > 1 and random.randint( 0, flips[1] ) == 0:
            image = image.transpose( Image.FLIP_TOP_BOTTOM )
            for m in meta:
                m2, m4 = m[2], m[4]
                m[4] = image.size[1] - m2
                m[2] = image.size[1] - m4
                
    origin_shift = ( offset[0] + tile_margin[0], offset[1] + tile_margin[1] )
    
    tile.paste( image, origin_shift )
    
    tile_count = 1

    # adjust meta
    # tile inherits all of image's offset meta data
    for m in meta:
        m[1] += origin_shift[0]
        m[2] += origin_shift[1]
        m[3] += origin_shift[0]
        m[4] += origin_shift[1]
    

    tile_meta.extend( meta )
    

    remaining_container_width = width - image_width
    remaining_container_height = height - image_height
    
    col_area = ( remaining_container_height * width )
    row_area = ( remaining_container_width * height )
    
    # choose orientation - go for the larger area
    if col_area > row_area:
        next_orientation = 2
    else:
        next_orientation = 3    
    

    next_off_x = offset[0] + image_width
    next_off_y = offset[1] + image_height  
    
    tiling_args = [
        # column first
        [ 
            [ 
                ( image_width, remaining_container_height ), 
                [ offset[0], next_off_y, 0 ]
            ], 
            [ 
                ( remaining_container_width, height ), 
                [ next_off_x, offset[1], 0 ]
            ] 
        ],
        # row first
        [ 
            [ 
                ( remaining_container_width, image_height ), 
                [ next_off_x, offset[1], 0 ]
            ],
            [ 
                ( width, remaining_container_height ), 
                [ offset[0], next_off_y, 0 ]
            ]
        ],
        # diagonal column first
        [ 
            [ 
                ( width, remaining_container_height ), 
                [ offset[0], next_off_y, 0 ]
            ], 
            [ 
                ( remaining_container_width, height ), 
                [ next_off_x, offset[1], 0 ]
            ] 
        ],
        # diagonal row first
        [ 
            [ 
                ( remaining_container_width, height ), 
                [ next_off_x, offset[1], 0 ]
            ],
            [ 
                ( width, remaining_container_height ), 
                [ offset[0], next_off_y, 0 ]
            ]
        ]
    ]
    
    # orient to smallest aperture
    if auto_orient:
        #if image_height < image_width:
        if col_area > row_area:
            orientation = 1
        else:
            orientation = 0
    else:
        # default is column first
        if orientation is None:
            orientation = 0
        
    tile_count_a = fill_tile( 
        container_size = tiling_args[ orientation ][0][0],
        offset = tiling_args[ orientation ][0][1], 
        items=items, 
        tile=tile,
        tile_margin=tile_margin, 
        tile_meta=tile_meta,
        no_meta=no_meta,
        auto_orient=auto_orient,
        orientation=orientation, 
        flips=flips,
        allow_diagonal=allow_diagonal
    )
    
    tile_count_b = fill_tile( 
        container_size=tiling_args[ orientation ][1][0],
        offset=tiling_args[ orientation ][1][1], 
        items=items, 
        tile=tile,
        tile_margin=tile_margin, 
        tile_meta=tile_meta,
        no_meta=no_meta,
        auto_orient=auto_orient,
        orientation=orientation, 
        flips=flips,
        allow_diagonal=allow_diagonal 
    )
    
    

    # if no tiles fit column/row then allow "diagonal" manoevre
    if tile_count_a == 0 and tile_count_b == 0 and allow_diagonal:
        
        tile_count_c = fill_tile( 
            container_size = tiling_args[ next_orientation ][0][0],
            offset = tiling_args[ next_orientation ][0][1], 
            items=items, 
            tile=tile,
            tile_margin=tile_margin, 
            tile_meta=tile_meta,
            no_meta=no_meta,
            auto_orient=auto_orient,
            orientation=orientation, 
            flips=flips,
            allow_diagonal=allow_diagonal
        ) 
        
        if tile_count_c == 0:
            tile_count_c = fill_tile( 
                container_size = tiling_args[ next_orientation ][1][0],
                offset = tiling_args[ next_orientation ][1][1], 
                items=items, 
                tile=tile,
                tile_margin=tile_margin, 
                tile_meta=tile_meta,
                no_meta=no_meta,
                auto_orient=auto_orient,
                orientation=orientation, 
                flips=flips,
                allow_diagonal=allow_diagonal
            )         
        
        return tile_count + tile_count_c
    else:
        return tile_count + tile_count_a + tile_count_b
"""

"""
def export_tiles( 
        tiles=None, 
        sort_by=None, 
        no_meta=None, 
        tile_prefix=None, 
        seq=0, 
        container_size=None, 
        output_size=None, 
        background_image_generator=None,
        tile_margin=(0,0,0,0),
        image_acceptor_factors=(0,0,0,0), 
        constraint=None,
        output_path=None,
        orientation=None,
        flips=None,
        auto_orient=True,
        allow_diagonal=True
    ):

    if output_size is None:
        output_size = container_size
        
    items_to_export = tiles if constraint is None else [ 
            item 
            for item in tiles 
            if constraint( item[1][0][1:5] )            
        ]

    
    random.shuffle( items_to_export )
    
    if sort_by:
        items_to_export.sort( key=sort_by )

    tile_id = 0
    
    num_tiles_exported = 0
    
    while len( items_to_export ) > 0:

        tile_id += 1
        tile_count = 0
        tile_meta = []
        tile_sources = []
        
        tile = Image.new( "RGB", container_size )
        
        if background_image_generator:
            background_image = background_image_generator()
            tile.paste( background_image )
            #tile.paste( background_image.resize( container_size, Image.ANTIALIAS ) )

        tile_count = fill_tile( 
                container_size=container_size, 
                offset=[ 0, 0, 0], 
                items=items_to_export, 
                tile=tile, 
                tile_margin=tile_margin,
                tile_meta=tile_meta,
                tile_sources=tile_sources,
                no_meta=no_meta,
                orientation=orientation,
                flips=flips,
                auto_orient=auto_orient,
                allow_diagonal=allow_diagonal
        )

        if tile_count > 0:
            if len( tile_meta ) > 0:
                write_tile( 
                    tile=[ tile, tile_meta, tile_sources ],
                    output_resolution=output_size,
                    tile_id=tile_id, 
                    tile_prefix="{}_{}".format( tile_prefix, seq ),
                    output_path=output_path
                )
                
                num_tiles_exported = num_tiles_exported + 1
        else:
            break
    
    return num_tiles_exported      
