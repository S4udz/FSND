# Casting Agency Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

The Casting Agency Project models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

This project provides a dedicated platform for practicing and showcasing a range of web development skills. These include data modeling, API design, authentication, authorization, and cloud deployment.
## Project Motivation
This project serves as a culmination of the skills I acquired throughout the FSND nanodegree program. It's an opportunity to apply concepts such as data modeling, API design, authentication, authorization, and cloud deployment in a real-world scenario.
## APP URL
https://fsnd-4ry4.onrender.com/
## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.


### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [render](https://www.render.com) is the cloud platform used for deployment

### Deploying the app on render

##### Steps:


1-Register an account on Render.
2-Set up a PostgreSQL database in your Render account, opting for the free tier plan.
3-Fork the repository, then create a web service on Render. Select "Build from GitHub repo" during the creation process.
4-Navigate to the environment section of your Render project and add the .env variables you configured, including the details of the Render PostgreSQL credentials.
5-Ensure that you set the environment variable PYTHON_VERSION to 3.7.1; failure to do so may result in a build failure.
6-Wait for the build process to complete.
7-Test the URL assigned to your web service, which should end with onrender.com.
8-Access the Render PostgreSQL database and execute the setup.psql script.
9-Validate the application's functionality by testing the API endpoints outlined below.
10-Congratulations! You're all set up.


### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the `capstone.psql` file provided. In terminal run:

```bash
createdb capstone
```

#### Running Tests
To run the tests, run
```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < setup.psql
python test_app.py
```

#### Auth0 Setup

You need to setup an Auth0 account.


#### .env Setup
your .env needs to have the following values:

* DATABASE_URL=
* DATABASE_USER=,
* DATABASE_PASSWORD =
* ASSISTANT_TOKEN = 
* PRODUCER_TOKEN =
* AUTH0_DOMAIN =  
* ALGORITHMS = 
* API_AUDIENCE = 

 you can set up these enviroment variables by configuring and running them in setup.sh
##### Roles

Create two roles for users under `Users & Roles` section in Auth0

* Casting Assistant
	* Can view actors and movies
* Executive Producer
	* All permissions a Casting Assistant
	* Add ,update ,and delete a movie from the database

##### Permissions

Following permissions should be created under created API settings.

* `get:actors`
* `get:movies`
* `patch:movies`
* `post:movies`
* `delete:movies`

##### Set JWT Tokens in `auth_config.json`

Use the following link to create users and sign them in. This way, you can generate 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

#### Launching The App


1. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
2. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = 'postgresql://{}:{}@{}/{}'.format(os.getenv("database_user"),os.getenv("database_password"),os.getenv("DATABASE_URL"), database_name)

    ```
**Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```
For more details [look at the documentation (31.1.1.2. Connection URIs)](https://www.postgresql.org/docs/9.3/libpq-connect.html)

5.  To run the server locally, execute:

    ```bash
    $ENV:FLASK_APP="app.py"
    flask run 
    ```


## API Documentation

### Models
There are two models:
* Movie
	* title
	* release_date
* Actor
	* name
	* age
	* gender

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

### Endpoints


#### GET /movies/id 
* Get a movie

* Require `get:movies` permission

* **Example Request:** curl http://localhost:5000/movies/1

* **Expected Result:**

``` json
{
    "associated_actors": [],
    "movie": {
        "id": 1,
        "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
        "title": "Movie 1"
    },
    "success": true
}
  ```

#### GET /actors/id
* Get an actor

* Requires get:actors permission

* **Example Request:** curl http://localhost:5000/actors/1

* **Expected Result:**
 ``` json
{
    "actor": {
        "age": 30,
        "gender": "Male",
        "id": 1,
        "name": "John Doe"
    },
    "associated_movies": [],
    "success": true
}
 ```
	
#### POST /movies
* Creates a new movie.

* Requires `post:movies` permission

* Requires the title and release date.

* **Example Request:** (Create)
    ```bash
	curl --location --request POST 'http://localhost:5000/movies' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"title": "test",
			"release_date": "19-02-2024"
		}'
    ``` 
* **Example Response:**
 ``` json
{
    "movie": {
        "id": 11,
        "release_date": "Tue, 12 Dec 2006 00:00:00 GMT",
        "title": "random4"
    },
    "success": true
}

```
#### DELETE /movies/id
* Deletes the movie with given id 

* Require `delete:movies` permission

* **Example Request:** `curl --request DELETE 'http://localhost:5000/movies/1'`

* **Example Response:**
    ```json
	{
		"deleted": 1,
		"success": true
    }
    ```

#### PATCH /movies/<movie_id>
* Updates the movie where <movie_id> is the existing movie id

* Require `update:movies` permission

* Responds with a 404 error if <movie_id> is not found

* Update the corresponding fields for Movie with id <movie_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/movies/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"title": "test"
        }`
  
    ```
  
*   **Example Response:**
   ```json
{
    "associated_actors": [],
    "movie": {
        "id": 1,
        "release_date": "Sat, 01 Jan 2022 00:00:00 GMT",
        "title": "Movie 1"
    },
    "success": true
}
```