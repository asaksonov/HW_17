# app.py
import json

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from config import app, db
from models import Movie
from schemas import MovieSchema

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route("/")
class MoviesViews(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        query = Movie.query
        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)

        return MovieSchema(many=True).dump(query.all()), 200

    def post(self):
        data = request.json
        try:
            db.session.add(
                Movie(**data)
            )
            db.session.commit()
        except Exception as e:
            print (e)
            db.session.rollback()

@movie_ns.route("/<int:id>/")
class MoviesViews(Resource):
    def get(self, id):
        result = db.session.query(Movie).filter(Movie.id == id).all()
        if len(result):
            return MovieSchema().dump(result[0]), 200
        else:
            return json.dumps({}), 200

    def put(self, id):
        data = request.json
        try:
            result = Movie.query.filter(Movie.id == id).one()

            result.title = data.get('title')
            result.description = data.get('description')
            result.trailer = data.get('trailer')
            result.year = data.get('year')
            result.rating = data.get('rating')
            result.genre_id = data.get('genre_id')
            result.director_id = data.get('director_id')

            db.session.add(result)
            db.session.commit()
            return 'Обновилось', 200
        except Exception:
            db.session.rollback()
            return 'Не обновилось', 500

    def delete(self, id):
        try:
            result = Movie.query.filter(Movie.id == id).one()

            db.session.delete(result)
            db.session.commit()
            return 'Удалили', 200
        except Exception:
            db.session.rollback()
            return 'Не удалили', 500

if __name__ == '__main__':
    app.run(port=8081, debug=True)
