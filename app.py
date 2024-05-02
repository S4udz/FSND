import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, actors_movies, add_actor_to_movie
from auth.auth import requires_auth, AuthError

def create_app(database_path=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()

    # Set up the database
    if database_path:
        setup_db(app, database_path)
    else:
        setup_db(app)

    # Enable CORS
    CORS(app)

    # Endpoint to get an actor by ID
    @app.route('/actors/<int:actor_id>', methods=["GET"])
    @requires_auth('get:actor')
    def get_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        movies = [movie.format() for movie in actor.movies]
        return jsonify({
            "success": True,
            "actor": actor.format(),
            'associated_movies': movies
        })

    # Endpoint to get a movie by ID
    @app.route('/movies/<int:movie_id>', methods=["GET"])
    @requires_auth('get:movie')
    def get_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        actors = [actor.format() for actor in movie.actors]
        return jsonify({
            "success": True,
            "movie": movie.format(),
            'associated_actors': actors
        })

    # Endpoint to add a new movie
    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movie')
    def post_movie(jwt):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        actors_id = body.get('actors_id')
        movie = Movie(title, release_date)
        if actors_id is not None:
            for actor_id in actors_id:
                actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
                if actor is None:
                    abort(404)
                movie.actors.append(actor)

        movie.insert()
        return jsonify({
            "success": True,
            "movie": movie.format()
        })

    # Endpoint to update a movie
    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('patch:movie')
    def patch_movie(jwt, movie_id):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        actors_id = body.get('actors_id')
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        associations = actors_movies.query.filter_by(movie_id=movie_id).all()
        for association in associations:
            association.delete()
        if actors_id is not None:
            for actor_id in actors_id:
                actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
                if actor is None:
                    abort(404)
                if actor not in movie.actors:
                    add_actor_to_movie(movie, actor)

        return jsonify({
            "success": True,
            "movie": movie.format(),
            "associated_actors": [actor.format() for actor in movie.actors]
        })

    # Endpoint to delete a movie
    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth('delete:movie')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            "success": True,
            "deleted": movie_id
        })

    # Error handlers
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'errorCode': '404',
            'message': 'The requested resource was not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'status': 'error',
            'errorCode': '400',
            'message': 'Bad request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'status': 'error',
            'errorCode': '500',
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

# Create the app
app = create_app(database_path=None)

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
