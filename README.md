# Cats adoption manager Restful API

RESTful API written using Flask python framework.
It helps to manage cat adoption.
Every user can post cats for adoption.
Every user can adopt other user's cats
## Developed endpoints
### General Notes
All the payloads of the following endpoints are in JSON format.
Some endpoints need the user credentials to be accessed.
The credentials of a given user are the access-token which is gotten from a login.
To login, username and password are required. For more information, read the User Endpoints documentation below
The access-token should be included in the "Authorization" header of the request. It should be: Bearer \<access-token\> (without <>).
catname keyword is a unique identifier for a given cat.
### User Endpoints
* \[GET\]: _/user/\<username\>_

      Returns information of a given user.
      If the request succeeds, the returned JSON will contain:
        - "first-name": the first name of the user
        - "last-name": the last name of the user
        - "user-id": the unique id of the user in the DB
        - "username": the unique username of the user
        - "address": the physical address of the user
        - "email": the e-mail of the user
        - "phone": the number phone of the user
        - "admin": a Boolean indicates if this user is a super user or not
        - "added-cats": array contains pairs of catname and the information of the cats added by this user
        - "adopted-cats": array contains pairs of catname and the information of the cats adopted by this user
        HTTP status code: 200
      If the user does not exist, the returned JSON will contain:
        - "message": "user not found"
        HTTP status code: 404
      Note: no access token is required to access this endpoint

* \[POST\]: _/user/\<username\>_

      Creates new user with the indicated username in the request.
      JSON payload attributes are:
        - "first-name": the first name of the user
        - "last-name": the last name of the user
        - "address": the physical address of the user
        - "password": the password of the user access
        - "email": the e-mail of the user (optional field)
        - "phone": the number phone of the user (optional field)
      If the request succeeds, the returned JSON will contain user information implemented above in the GET endpoint
        HTTP status code: 200
      If the user has already exist, the returned JSON will contain:
        - "message": "the user has already existed"
        HTTP status code: 400
      Note: no access token is required for this endpoint

* \[PUT\]: _/user/\<username\>_

      Assigns or reassigns any user attribute or information
      JSON payload can contain one or more of the following attributes:
        - "first-name": the first name of the user
        - "last-name": the last name of the user
        - "address": the physical address of the user
        - "password": the password of the user access
        - "email": the e-mail of the user
        - "phone": the number phone of the user
      If the request succeeds, the JSON will contain the user information implemented in the GET endpoint`
        HTTP status code: 200
      If permission denied, the JSON will contain:
        - "message": "Not permitted action"
        HTTP status code: 401
      Note: This endpoint can only modify an existing user. However, it can not create new one.
            a given user cannot change other user information
            super users can change other users information
            Access token is required for this endpoint


* \[DELETE\]: _/user/\<username\>_

      Deletes an existing user.
      If the request succeeds, the returned JSON will contain:
        - "message": "user deleted"
        HTTP status code: 202
      If the user does not exist, the returned JSON will contain:
        - "message": "the requested user is not found"
        HTTP status code: 404
      If permission denied, the returned JSON will contain:
        -  "message": "permission is not permitted. You need admin privileges to delete a user"
        HTTP status code: 400
      Note: a given user can delete himself. However other users cannot delete other users accounts
            super users can delete others user accounts
            Access token is required for this endpoint

* \[POST\]: _/login/\<username\>_

      Logins a User
      JSON payload must contain:
        - "password": string which contains the user's password
      If successfully logged in you get JSON contains:
        - "message": "Logged in as <username>"
        - "access-token": long string remains valid for only 15 minutes. It gives the user the authorization to access other endpoints.
        - "refresh-token": long string remains valid longer than the access token (1 hour). It helps to generate a new access token.
        HTTP status code: 200
      If the login fails you get JSON contains:
        - "message": "username or password is not correct"
        HTTP status code: 400

* \[POST\]: _/refresh_

      This endpoint acts like a helper. It generates a new access token using a refresh token.
      Note: a refresh token is required in the header of the request.

* \[POST\]: _/user/grant/\<username\>_

      Gives admin privileges to a user who is identified by \<username\>
      To grant admin privileges to other users, the request maker should be a super user.
      If the request maker is not an admin, they get JSON contains:
        - "message": "You must be a super user to grant privileges to other users"
        HTTP status code: 400
      If the request is made successfully, the JSON payload will contain:
        - "message": "<username> is now an admin"
        HTTP status code: 200
      If the requested user does not exist, the JSON payload will contain:
        - "message": "The requested user does not existed"
        HTTP status code: 404
      Note: an access token of an admin user in the header of the request and an existing username are required to successfully make the request

* \[POST\]: _/adopt/\<catname\>_

      The main endpoint of this RESTful API
      It helps a given user to adopt a non-adopted cat which is identified <catname>
      If the request succeeds, the returned JSON payload will contain:
        - "message": "congratulations ! Thank you for adopting \<username\>"
        HTTP status code : 200
      If the cat has already adopted, the returned JSON payload will contain:
        - "message": "This cat has already adopted ! Thanks anyway"
        HTTP status code : 400
      If the requested cat doesn't exist, the returned JSON payload will contain:
        - "message": "could not find the requested cat"
        HTTP status code: 404
      Note: an access token is required

* \[GET\]: _/users_

      Returns all users information.
      If the request succeeds, the returned JSON payload will contain:
        - "users": array contains key-value pairs. every key-value pair is a username and another JSON contains all information about this user
        HTTP status code: 200
      If the request fails, the returned JSON will contain:
        - "message": "Permission denied"
        HTTP status code: 401
      Note: an access token of an admin user is required to access this endpoint

* \[GET\]: _/taken/\<username\>_

      Indicates if a username has already taken or not. This endpoint is useful to tell the new user if this username is available or not before he creates his account
      If the username has already been taken, the returned JSON will contain:
        - "taken": true
        HTTP status code: 400
      If the username is available, the returned JSON will contain:
        - "taken": false
        HTTP status code: 200
      Note: no access token is required to access this endpoint

### Cat Endpoints
* \[GET\]: _/cat/\<catname\>_

      Returns information of the cat which is identified by \<catname\>
      If the request succeeds, the returned JSON will contain key-value pair.
      The key is \<catname\> and the value is another JSON that contains:
        - "name": the name of the cat
        - "img_url": the URL of its picture
        - "adopted": a Boolean indicates if the cat was adopted or not
        - "sex": its sex. It should be a character. "F" for female and "M" for male
        - "color": string describes its colors
        - "age-year": integer indicates the number of year has been lived by the cat
        - "age-month": integer indicates the number of months has been lived by the cat
        - "age-day": integer indicates the number of days has been lived by the cat
        - "owner-id": the ID of the user who added this cat
        - "owner-username": the username of the user who added this cat
        - "owner-name": the full name (first name and last name) of the user who added this cat
        If the cat has already adopted this value will hold more attributes:
          - "adopter-id": the ID of the user who adopted this cat
          - "adopter-username": the username of the user who adopted this cat
          - "adopter-name": the full name (first name and last name) of the user who adopted this cat
          HTTP status code: 200

      Notes: the age-year, age-month and age-day will be combined to determine how long the cat has been lived

* \[POST\]: _/cat/\<catname\>_

      Creates a new Cat object and stores it in the DB
      JSON payload must contain:
        - "name": the name of the cat
        - "img_url": the URL of its picture
        - "adopted": a Boolean indicates if the cat was adopted or not
        - "color": string describes its colors
        - "sex": its sex. It should be a character. "F" for female and "M" for male
        - "age-year": integer indicates the number of year has been lived by the cat (optional)
        - "age-month": integer indicates the number of months has been lived by the cat (optional)
        - "age-day": integer indicates the number of days has been lived by the cat (optional)
      If the request succeeds, the returned JSON will hold a key-value pair has the same attributes implemented above in the GET endpoint
        HTTP status code: 201
      If the catname has already been taken, the returned JSON will contain:
        - "message": "This catname has already taken"
        HTTP status code: 400
      Note: access token is required to access this endpoint (You should login)

* \[PUT\]: _/cat/\<catname\>_

      Assigns or reassigns any user attribute or information
      JSON payload can contain one or more of the following attributes:
        - "name": the name of the cat
        - "img_url": the URL of its picture
        - "adopted": a Boolean indicates if the cat was adopted or not
        - "color": string describes its colors
        - "sex": its sex. It should be a character. "F" for female and "M" for male
        - "age-year": integer indicates the number of year has been lived by the cat
        - "age-month": integer indicates the number of months has been lived by the cat
        - "age-day": integer indicates the number of days has been lived by the cat
      If the request succeeds, the returned JSON will hold a key-value pair has the same attributes implemented above in the GET endpoint
        HTTP status code: 200
      If the cat does not exist, the returned JSON will contain:
        - "message": "cat not found"
        HTTP status code: 404
      Note: This endpoint can only modify an existing user. However, it can not create new one.
            Access token is required for this endpoint

* \[DELETE\]: _/cat/\<catname\>_

      Deletes an existing cat.
      Note: a given user can delete his cat. However other users cannot delete other users cats
            super users can delete others cats
            Access token is required for this endpoint

* \[GET\]: _/cats_

      List all available cats
      If the request succeeds, the returned JSON payload will contain:
        - "cats": array contains key-value pairs. every key-value pair is a catname and another JSON contains all information about this cat
          HTTP status code: 200
      Note: no access token is required to access this endpoint

* \[GET\]: _/cats_

      List all adopted cats
      If the request succeeds, the returned JSON payload will contain:
        - "adopted-cats": array contains key-value pairs. every key-value pair is a catname and another JSON contains all information about this cat
        HTTP status code: 200s
      Note: no access token is required to access this endpoint

* \[GET\]: _/isadopted/\<catname\>_

      Returns a message indicates if the cat has already been adopted or not.
      If the cat has already been adopted, the returned JSON will contain:
        - "message": "This cat is adopted by \<The Full name of the adopter\>"
        HTTP status code: 200
      If the cat is not adopted, the returned JSON will contain:
        - "message": "This cat is not adopted by anyone. Please adopt it"
        HTTP status code: 400
      If the cat does not exist, the returned JSON will contain:
        - "message": "Could not find the requested cat"
        HTTP status code: 404
      Note: no access token is required to access this endpoint

* \[GET\]: _/taken/\<catname\>_

      Indicates if a catname has already taken or not. This endpoint is useful to tell the user if the catname is available or not before he creates a cat object
      If the catname has already been taken, the returned JSON will contain:
        - "taken": true
        HTTP status code: 400
      If the catname is available, the returned JSON will contain:
        - "taken": false
        HTTP status code: 200
      Note: no access token is required to access this endpoint

## Python dependencies
* Flask

      $ pip install Flask

* Flask-RESTful

      $ pip install Flask-RESTful
* Flask-SQLAlchemy

      $ pip install Flask-SQLAlchemy
* Flask-JWT

      $ pip install Flask-JWT
* uwsgi

      $ pip install uwsgi
* psycopg2

      $ pip install psycopg2
* passlib

      $ pip install passlib

## Deployment
All Heruko configuration files are included

You can simply deploy the application to Heruko by connecting to github.
## License
The content of this repository is licensed under a [Creative Commons Attribution License](https://creativecommons.org/licenses/by/3.0/us/)
