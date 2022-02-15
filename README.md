# PACKAGES-TO-GO: Back-end Layer 


## Description

- This  is a package delivery management application,  created as a Capstone project for Ada Developer Academy.  It aims to help buildings to manage their  resident's incoming packages and delivery requests.
- This app allows  the manager's account to create a list of packages, associate each package with its owner, update package information, view package information and delete package information when the package is  delivered successfully.
- This app also allows the resident's account to access/view  the packages and request delivery.


## Setting Up Development

- Create a database:
- Creating a .env File
- Create a file named .env.
- Create two environment variables that will hold your database URLs.

- SQLALCHEMY_DATABASE_URI to hold the path to your development database

- Run $ flask db init
- Run $ flask db init.

### Run Code
        Run $ flask run or $ FLASK_ENV=development flask run

- We can run the Flask server specifying that we're working in the development environment. This enables hot-reloading, which is a feature that refreshes the Flask server every time there is a detected change.

        $ FLASK_ENV=development flask run



# Endpoints

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