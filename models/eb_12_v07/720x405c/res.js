res = {
    
    "abort": false,
    
    "data": "eb_12_v07",
    "model":"720x405c",     
    
    "output_resolution": [ 720, 405 ],
    
    
    "background_classes": [ "unclassified" ],     
    
    "product": {
        "parts": [ "eval", "train" ],
        "scaled": [ 
           [ "g", [ 720, 405 ], 0.2 ],
           [ "m", [ 960, 540 ], 0.2 ],
           [ "s", [ 1600, 900 ], 0.2 ],
           [ "x", [ 1920, 1080 ], 0.2 ]
        ], 
        
        "tiled": [
            {
                "crop": [ 100, 100 ], 
                "key": "tight", 
                "pad": 50,
                
                "apertures": [
                    [ "g", [ 720, 405 ], 0.2, 1 ],
                    [ "m", [ 960, 540 ], 0.2, 1 ],
                    [ "s", [ 1600, 900 ], 0.2, 1 ], 
                    [ "x", [ 1920, 1080 ], 0.2, 1 ]
                ]
            }
        ]
    },
    
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
}
