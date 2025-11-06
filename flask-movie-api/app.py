#Jhoram Narsico

from flask import Flask
from flask_restful import reqparse, Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
api = Api(app)

class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movie(title='{self.title}', director='{self.director}', release_year={self.release_year})"

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title of the movie is required', required=True)
parser.add_argument('director', type=str, help='Director of the movie is required', required=True)
parser.add_argument('release_year', type=int, help='Release year of the movie is required', required=True)

class Movie(Resource):
    def get(self, movie_id):
        movie = MovieModel.query.get(movie_id)
        if movie:
            return {'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year}
        return {'message': 'Movie not found'}, 404

    def delete(self, movie_id):
        movie = MovieModel.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'Movie deleted successfully'}
        return {'message': 'Movie not found'}, 404

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

class MovieList(Resource):
    def get(self):
        movies = MovieModel.query.all()
        return [{'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year} for movie in movies]

    def post(self):
        args = parser.parse_args()
        new_movie = MovieModel(title=args['title'], director=args['director'], release_year=args['release_year'])
        db.session.add(new_movie)
        db.session.commit()
        return {'id': new_movie.id, 'title': new_movie.title, 'director': new_movie.director, 'release_year': new_movie.release_year}, 201

api.add_resource(MovieList, '/movies')
api.add_resource(Movie, '/movies/<int:movie_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)