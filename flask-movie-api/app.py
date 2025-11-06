# app.py

from flask import Flask
from flask_restful import reqparse, Api, Resource
from flask_sqlalchemy import SQLAlchemy

# 1. Initialize the Flask Application
app = Flask(__name__)

# 2. Configure the SQLite Database
# This will create a file named 'movies.db' in your project folder.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
# This disables a feature that signals the application every time a change is about to be made in the database.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
api = Api(app)


# 3. Define the Movie Database Model
# This class defines the structure of the 'movies' table in our database.
class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movie(title='{self.title}', director='{self.director}', release_year={self.release_year})"


# 4. Define the Request Parser
# This will validate the data sent in POST and PATCH requests.
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title of the movie is required', required=True)
parser.add_argument('director', type=str, help='Director of the movie is required', required=True)
parser.add_argument('release_year', type=int, help='Release year of the movie is required', required=True)


# 5. Define API Resources
# A "Resource" is a class that handles requests for a specific endpoint (e.g., /movies/1)

# Resource for a single movie item (e.g., GET, PATCH, DELETE a specific movie)
class Movie(Resource):
    # GET a single movie by its ID
    def get(self, movie_id):
        movie = MovieModel.query.get(movie_id)
        if movie:
            return {'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year}
        return {'message': 'Movie not found'}, 404 # Return a 404 Not Found error if the movie doesn't exist

    # DELETE a movie by its ID
    def delete(self, movie_id):
        movie = MovieModel.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'Movie deleted successfully'}
        return {'message': 'Movie not found'}, 404

    # PATCH (update) a movie by its ID
    def patch(self, movie_id):
        movie = MovieModel.query.get(movie_id)
        if movie:
            args = parser.parse_args()
            movie.title = args['title']
            movie.director = args['director']
            movie.release_year = args['release_year']
            db.session.commit()
            return {'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year}
        return {'message': 'Movie not found'}, 404

# Resource for a list of movies (e.g., GET all movies, POST a new movie)
class MovieList(Resource):
    # GET all movies
    def get(self):
        movies = MovieModel.query.all()
        return [{'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year} for movie in movies]

    # POST a new movie
    def post(self):
        args = parser.parse_args() # This will parse and validate the incoming JSON payload
        new_movie = MovieModel(title=args['title'], director=args['director'], release_year=args['release_year'])
        db.session.add(new_movie)
        db.session.commit()
        return {'id': new_movie.id, 'title': new_movie.title, 'director': new_movie.director, 'release_year': new_movie.release_year}, 201 # Return 201 Created status


# 6. Add Resources to the API and Define Endpoints
api.add_resource(MovieList, '/movies')
api.add_resource(Movie, '/movies/<int:movie_id>')


# 7. Run the Flask Application
if __name__ == '__main__':
    # This block ensures that the database tables are created before the first request.
    with app.app_context():
        db.create_all()
    app.run(debug=True)