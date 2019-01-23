res = {
    "abort":false, 
    
    "background_classes":[ "unclassified" ], 
    
    "data":"eb_12_v07", 
    
    "model":"320x180c", 
    
    "output_resolution":[ 320, 180 ], 
    
    
    "product":{
        
        "parts": [ "eval", "train" ],
        
        "scaled":[
            [ "g", [ 480, 270 ], 0.2 ], 
            [ "m", [ 960, 540 ], 0.2 ], 
            [ "s", [ 1600, 900 ], 0.2 ], 
            [ "x", [ 1920, 1080 ], 0.2 ]
        ], 
        
        "tiled":[
            {
                "apertures":[
                    [ "m", [ 960, 540 ], 0.2, 2 ], 
                    [ "s", [ 1440, 810 ], 0.2, 4 ], 
                    [ "t", [ 1600, 900 ], 0.2, 6 ], 
                    [ "x", [ 1920, 1080 ], 0.2, 8 ]
                ], 
                "crop":[ 100, 100 ], 
                "key":"tight", 
                "pad":120
            }
        ]
    }, 
    
    
    "training_records":{
        "eval":{
            "filename":"eval.record", 
            "num_shards":1
        }, 
        "train":{
            "filename":"train.record", 
            "num_shards":10
        }
    }
}
