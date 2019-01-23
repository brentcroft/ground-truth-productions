"""

    Common library imports
"""
import os
import io
import pandas as pd
import random
from PIL import Image
import contextlib2
from collections import namedtuple, OrderedDict
"""

    TensorFlow imports
"""
import tensorflow as tf
from object_detection.utils import dataset_util
from object_detection.dataset_tools import tf_record_creation_util
"""



"""
def create_tf_example( group, path, category_numbers ):
    
    for index, row in group.object.iterrows():
        folder = row['folder']
    
    if folder is None:
        raise ValueError("No folder attribute in data")
    
    with tf.gfile.GFile(os.path.join(path, '{}'.format(folder), '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
        
    encoded_jpg_io = io.BytesIO(encoded_jpg)

    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []
    
    #print( "Processing: {}".format( group.filename ) )

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append( category_numbers[ row['class'] ] )
        
        item_no = row['item']
        class_name = row['class']
        category_number = category_numbers[ class_name ]
        
        #print( "  added object: {}: {}={}".format( item_no, class_name, category_number ) )        

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example
"""



"""
def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]
"""



"""
def processCsvFileShards( csv_input=None, xsheet=None, image_root=None, output_path=None, category_numbers=None, num_shards=10 ):

    if num_shards < 1:
        raise ValueError( "num_shards must be greater than 0".format( num_shards ) )

    examples = xsheet if csv_input is None else pd.read_csv( csv_input )         
    grouped = split( examples, 'filename' )
    random.shuffle( grouped )
        
    if num_shards == 1:
        with tf.python_io.TFRecordWriter( output_path ) as writer:
            for group in grouped:
                tf_example = create_tf_example( group, image_root, category_numbers )
                writer.write( tf_example.SerializeToString() )
        
        print('Created TFRecord: items={}, destination={}'.format( len( grouped ), output_path ) )
        
    else:        
        with contextlib2.ExitStack() as tf_record_close_stack:
            output_tfrecords = tf_record_creation_util.open_sharded_output_tfrecords(
                tf_record_close_stack, 
                output_path, 
                num_shards )

            index = 0
            for group in grouped:
                tf_example = create_tf_example( group, image_root, category_numbers )
                output_shard_index = index % num_shards
                output_tfrecords[ output_shard_index ].write( tf_example.SerializeToString() )
                index = index + 1
                
            print('Created TFRecord: items={}, shards={}, destination={}'.format( len( grouped ), num_shards, output_path ) )