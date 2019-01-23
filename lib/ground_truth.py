"""
    Read/write ground truth meta-data to XML files.
    Extended Pascal/VOC format with additional attributes
    
    Ingest meta-data to existing meta-data
    
"""
from lxml import etree as ET
"""

    None becomes the empty string
"""
def write_attributes_to_element( parent_element, attributes, use_attributes_element = True, use_attribute_element = True ):
    if attributes is not None and len( attributes ) > 0:
        if use_attributes_element:
            attributes_element = ET.SubElement( parent_element, 'attributes')
        else:
            attributes_element = parent_element

        for attr in attributes:
            if use_attribute_element:
                attribute_element = ET.SubElement( attributes_element, 'attribute')
                attribute_element.set( "key", attr )
            else:
                attribute_element = ET.SubElement( attributes_element, attr )
            
            value = "" if attributes[ attr ] is None else str( attributes[ attr ] ) 
            attribute_element.text = str( value )
"""


"""
def maybe_number(value):
    try:
        try:
            return int(value)
        except:
            return float(value)
    except:
        return value
"""

    the empty string becomes None
"""
def read_attributes_from_element( parent_element, attributes={} ):
    try:
        attributes_element = parent_element.find("attributes")
        if attributes_element is not None:
            for attribute_element in attributes_element.findall("attribute"):
                value = attribute_element.text
                if value == "" or value == "None":
                    value = None
                attributes[ attribute_element.get( "key" ) ] = maybe_number( value )
    except Exception as e:
        print( "Failed to read attributes: {}".format( e ) )
    return attributes
"""


"""
def get_file_meta( classification_file ):
    root = ET.parse( classification_file ).getroot()
    
    file_attributes = {}
    read_attributes_from_element( root, file_attributes )
    
    filename = root.find('filename').text
    
    if root.find('folder') is None:
        folder = None
    else:
        folder =  root.find('folder').text
        
    if root.find('path') is None:
        path = None 
    else:
        path = root.find('path').text
    
    size = root.find('size')
    width, height, depth = int(size.find('width').text), int(size.find('height').text), int(size.find('depth').text)
    item = 0    
    labeled_objects = []
    for member in root.findall('object'):
        class_name = member.find('name').text
        if member.find('score') is None:
            score = 0
        else:
            score = float( member.find('score').text )
        category_box = member.find( 'bndbox' )
        
        object_attributes = read_attributes_from_element( member )
        
        category_object = { 
            "name": class_name, 
            "box": ( 
                int(category_box[0].text), 
                int(category_box[1].text), 
                int(category_box[2].text), 
                int(category_box[3].text)
            ),
            "score": score,
            "item": item,
            "attributes": object_attributes
        }
        labeled_objects.append( category_object )
        item = item + 1

    return {
        "filename": filename,
        "folder": folder,
        "path": path,
        "size": ( width, height, depth ),
        "objects": labeled_objects,
        "attributes": file_attributes
    }
"""

    write a new classification file given meta-data
"""
def put_file_meta( classification_file, meta_data ):
    root = ET.Element( 'annotation' )
    
    if 'folder' in meta_data:
        ET.SubElement( root, 'folder' ).text = meta_data['folder']
        
    if 'filename' in meta_data:
        ET.SubElement( root, 'filename' ).text = meta_data['filename']
    
    if "path" in meta_data:
        ET.SubElement( root, 'path' ).text = meta_data['path']

    if "size" in meta_data:
        sizeE = ET.SubElement( root, 'size' )
        widthE, heightE, depthE = \
                ET.SubElement( sizeE, 'width' ), \
                ET.SubElement( sizeE, 'height' ), \
                ET.SubElement( sizeE, 'depth' )
        
        size = meta_data['size']
        widthE.text = str( size[0] ) 
        heightE.text = str( size[1] )
        depthE.text = str( size[2] ) 

    #print( 'meta_data["objects"]: {}'.format( meta_data["objects"] ) )        
    for item in meta_data["objects"]:
        try:
            objectE = ET.SubElement( root, 'object' )
            
            ET.SubElement( objectE, 'name' ).text = item["name"]

            xmin, ymin, xmax, ymax = item["box"]

            if 'score' in item and item["score"] is not None:
                ET.SubElement( objectE, 'score' ).text = str( item["score"] )

            # create elements
            bndboxE = ET.SubElement( objectE, 'bndbox' )
            xminE, yminE = ET.SubElement( bndboxE, 'xmin' ), ET.SubElement( bndboxE, 'ymin' )
            xmaxE, ymaxE = ET.SubElement( bndboxE, 'xmax' ), ET.SubElement( bndboxE, 'ymax' )


            bndboxE[0].text = str( xmin )
            bndboxE[1].text = str( ymin )
            bndboxE[2].text = str( xmax )
            bndboxE[3].text = str( ymax ) 
            
            if "attributes" in item:
                write_attributes_to_element( objectE, item["attributes"])

        except Exception as e:
            print( "BAD_OBJECT: {}\n {}".format( item, e ) )
            raise e
    
    if "attributes" in meta_data:
        write_attributes_to_element( root, meta_data["attributes"] )
    
    root.getroottree().write( classification_file, pretty_print=True )
"""


""" 
def rect_area( r ):
    return ( r[2] - r[0] ) * ( r[3] - r[1] )
"""


""" 
def rect_overlap_area( r1, r2 ):
    x_overlap = max( 0, min( r1[2], r2[2] ) - max( r1[0], r2[0] ) )
    y_overlap = max( 0, min( r1[3], r2[3] ) - max( r1[1], r2[1] ) )
    return x_overlap * y_overlap
"""

    gets the overlap from two box containers
"""
def rect_overlap_areas( cl1, cl2 ):
    return [
        rect_area( cl1["box"] ),
        rect_area( cl2["box"] ),
        rect_overlap_area( cl1["box"], cl2["box"] )
    ]
"""


"""  
def remove_attr( target, attribute_names ):
    for attr in attribute_names:
        if attr in target:
            del target[ attr ]
"""


"""         
def rename_class( gt_meta, old_name=None, new_name=None ):
    if old_name is None or new_name is None:
        raise ValueError( "Null args: old_name={}, new_name{}".format( old_name, new_name ) )

    num_replaced = 0;
    
    for g in gt_meta["objects"]:
        if g["name"] == old_name:
            g["name"] = new_name
            num_replaced = num_replaced + 1
    
    return num_replaced
"""

    maybe update gt_meta by looking at inf_meta
"""
def ingest_inference_meta( gt_meta, inf_meta, min_overlap=0.9, min_glitch_score=0.1, min_untruth_score=0.5 ):

    # new list of gt objects
    ground_truth_objects = [ gt for gt in gt_meta["objects"] ]

    # list of inf objects
    inference_classification = None
    inference_classification_objects = inf_meta["objects"]

    for g in ground_truth_objects:
        # area details plus the object pair
        all_overlaps = [ 
            ( rect_overlap_areas( g, i ), i ) 
            for i in inference_classification_objects
        ]
        
        # overlapping_objects are consumed
        # what percentage of the gt box is overlapped
        overlapping_objects = [
            mo
            for mo in all_overlaps
            if abs( mo[0][0] - mo[0][1] ) < (mo[0][0] * min_overlap)
            and mo[0][2] > (mo[0][0] * min_overlap)
        ]
        
        # new list only has high scoring boxes
        scoring_overlapping_objects = [
            mo
            for mo in overlapping_objects
            if mo[1]["score"] >= min_glitch_score
        ]

        gt_attr = g["attributes"]
        
        # set to zero
        g["score"] = 0
        gt_attr["box-score"] = 0 
        gt_attr["cardinality"] = 0  
        gt_attr["class-error"] = ""
        gt_attr["class-error-score"] = 0
                
        if len( scoring_overlapping_objects ) > 0:

            # deal with class matches first
            class_matches = [ 
                mo 
                for mo in scoring_overlapping_objects 
                if mo[1]["name"] == g["name"]
            ]
            
            if len( class_matches ) > 0:
                # pick highest scoring
                # TODO: losing information from dupicate boxes
                class_match = max( class_matches, key=lambda mo: mo[0][2] )
                
                # unpack area details
                # and the selected inf object
                gt_area, inf_area, overlap_area = class_match[ 0 ]
                inf_object = class_match[ 1 ]   

                # copy inference and overlap scores
                g["score"] = inf_object["score"]
                gt_attr["box-score"] = int( overlap_area / gt_area * 100 )     

                gt_attr["cardinality"] = len( class_matches )

            
            # deal with non-class matches second                
            non_class_matches = [ 
                mo 
                for mo in scoring_overlapping_objects 
                if mo[1]["name"] != g["name"]
            ]
                
            if len( non_class_matches ) > 0:
                # negative cardinality
                gt_attr["cardinality"] = ( -1 * len( non_class_matches ) ) + gt_attr["cardinality"]
                gt_attr["class-error"] = ", ".join( [ 
                    "{}({:.2f})".format( mo[1]["name"], mo[1]["score"] ) 
                    for mo in non_class_matches 
                ] )
                
                class_error_scores = [ mo[1]["score"] for mo in non_class_matches ]
                gt_attr["class-error-score"] = sum( class_error_scores ) / float( len( class_error_scores ) )
                

        # we've now dealt with the overlapping inference objects
        for oo in overlapping_objects:
            inference_classification_objects.remove( oo[1] ) 

            
    # global in file
    gt_meta_attr = gt_meta["attributes"]
    
    # clean up attr
    attr_to_remove = [ "untruth_count", "comment" ]
    for attr in attr_to_remove:
        if attr in gt_meta_attr:
             del gt_meta_attr[attr] 
    
    # write new attr
    gt_meta["attributes"]["untruth"] = ""
    gt_meta["attributes"]["untruth-count"] = 0

    # any untruth discovered in image
    if len( inference_classification_objects ) > 0:
        hotspots = [
            inf_object["name"]
            for inf_object in inference_classification_objects
            if inf_object["score"] >= min_untruth_score
        ]
        
        gt_meta["attributes"]["untruth"] = "{}".format( str( hotspots ) )
        gt_meta["attributes"]["untruth-count"] = len( hotspots )
