cfg = {
    "cn": {
        "host":"0.0.0.0",
        "port":8080,
    },
    
    "root":{
        "name":"root",
        "pw":"0000",
        
    },
    "wUser":{
        "wUser":"Node", # watch only user.
        "wUserToken":[ # to limit read only acces we use tokens to grant access
            "2876665379"
        ],
    },
    
    "dir":{
        "DbRootDir":"./db"  # pls provide full path ("./" is current directiony)
    }    

}