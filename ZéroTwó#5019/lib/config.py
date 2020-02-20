cfg = {
    "cn": {
        "host":"0.0.0.0",
        "port":3600,
    },
    
    "root":{
        "name":"root",
        "pw":"0000",
        
    },

    "users":[
        "override:ov123"
    ],

    "wUser":{
        "wUser":"Node", # watch only user.
        "wUserToken":[ # to limit read only access we use tokens to grant access
            "2876665379"
        ],
    },
    
    "dir":{
        "DbRootDir":"./db"  # please provide full path ("./" is current directiony)
    }    

}