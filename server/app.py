#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = []
        for plant in plants:
            plant_data = {
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price
            }
            plant_list.append(plant_data)
        return jsonify(plant_list)

    def post(self):
        data = request.json
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if name is None or image is None or price is None:
            return {'error': 'Missing required fields'}, 400

        new_plant = Plant(
            name=name,
            image=image,
            price=price
        )
        db.session.add(new_plant)
        db.session.commit()
        return {
            'id': new_plant.id,
            'name': new_plant.name,
            'image': new_plant.image,
            'price': new_plant.price
        }, 201

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        plant_data = {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        }
        return jsonify(plant_data)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
