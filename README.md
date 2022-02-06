# PACKAGES-TO-GO: Back-end Layer 



## Create - new user 

    endpoint -> https://localhost:5000/users
    Request Body -> 
    
    {
    "name": "Emanueli",
    "unit": "1498",
    "email": "manuo@gmail.com",
    "phone_number": "(585)599-2380"
    }
    
    Response Body ->

    {
    "email": "manuo@gmail.com",
    "name": "Emanueli",
    "phone_number": "(585)599-2380",
    "status": false,
    "unit": "1498",
    "user_id": 4
    }

## Read - all users 
    Endpoint -> https://localhost:5000/users

    Response body ->

    [
       {
    "email": "manuo@gmail.com",
    "name": "Emanueli",
    "phone_number": "(585)599-2380",
    "status": false,
    "unit": "1498",
    "user_id": 4
    }
    ,
    {
    "email": "rita@gmail.com",
    "name": "Rita",
    "phone_number": "(585)599-2380",
    "status": false,
    "unit": "6754",
    "user_id": 1
    } 
    ]