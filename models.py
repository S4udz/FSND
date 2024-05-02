import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

# Define the database name and construct the database URL using environment variables
database_name = 'capstone'
database_path = 'postgresql://{}:{}@{}/{}?sslmode=prefer'.format(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), database_name)

# Instantiate SQLAlchemy
db = SQLAlchemy()

"""
setup_db(app)
    Binds a Flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    # Configure the Flask app with the database URL
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Bind the SQLAlchemy instance to the Flask app
    db.app = app
    db.init_app(app)
    # Create all database tables
    db.create_all()

# Helper function to add an actor to a movie and commit it to the database
def add_actor_to_movie(movie, actor):
    movie.actors.append(actor)
    # Add the modified movie object to the session
    db.session.add(movie)
    # Commit the changes to the database
    db.session.commit()

# Define the association table for actors and movies
class actors_movies(db.Model):
    __tablename__ = 'actors_movies'

    id = Column(Integer, primary_key=True)
    actor_id = Column("actor_id", Integer, db.ForeignKey('Actor.id'))
    movie_id = Column("movie_id", Integer, db.ForeignKey('Movie.id'))

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Define the Movie table
class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    actors = db.relationship('Actor', secondary='actors_movies', lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

# Define the Actor table
class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship('Movie', secondary='actors_movies', lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
