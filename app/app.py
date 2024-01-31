from flask import Flask, request, make_response,jsonify, abort
from flask_restful import Resource, Api
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Creating Routes

# Index/Home Route
class Home(Resource):
    def get(self):
        response_dict = {
            "home": "Welcome to Pizza/Restaurants API"
        }
        response = make_response(
            jsonify(response_dict),
            200
        )
        return response
    
api.add_resource(Home, '/')    

# GET/restaurants Route
class Restaurants(Resource):
    def get(self):
        restaurants = []
        for restaurant in Restaurant.query.all():
            restaurant_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            restaurants.append(restaurant_dict)
        return make_response(
            jsonify(restaurants),
            200
        )    

api.add_resource(Restaurants, '/restaurants')


# GET/DELETE/restaurants/:id Route

from flask import jsonify, make_response, abort
from flask_restful import Resource
from models import db, Restaurant, RestaurantPizza

class RestaurantsId(Resource):
    def get(self, id): 
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            restaurant_dict = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": []
            }

            for restaurant_pizza in restaurant.restaurant_pizzas:
                pizza_dict = {
                    "id": restaurant_pizza.pizza.id,
                    "name": restaurant_pizza.pizza.name,
                    "ingredients": restaurant_pizza.pizza.ingredients
                }
                restaurant_dict["pizzas"].append(pizza_dict)

            return make_response(
                jsonify(restaurant_dict),
                200
            )
        else:
            return make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            # Delete associated RestaurantPizza instances
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()

            # Delete the restaurant
            db.session.delete(restaurant)
            db.session.commit()

            return jsonify(message="Restaurant deleted successfully"), 204
        else:
            abort(404, description="Restaurant not found")


api.add_resource(RestaurantsId, '/restaurants/<int:id>')


# GET/pizzas Route
class Pizzas(Resource):
    def get(self):
        pizzas = []

        for pizza in Pizza.query.all():
            pizza_dict = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            pizzas.append(pizza_dict)
        return make_response(
            jsonify(pizzas),
            200
        )  

api.add_resource(Pizzas, '/pizzas')

# POST /restaurant_pizzas Route
class RestaurantPizzas(Resource): 
    def post(self):
        data = request.json

    # Validate input data
        if not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']):
            return jsonify({"errors": ["validation errors"]}), 400

    # Check if Pizza and Restaurant exist
        pizza = Pizza.query.get(data['pizza_id'])
        restaurant = Restaurant.query.get(data['restaurant_id'])

        if not pizza or not restaurant:
            return jsonify({"errors": ["validation errors"]}), 400

    # Create new RestaurantPizza
        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza=pizza,
                restaurant=restaurant
            )

            db.session.add(restaurant_pizza)
            db.session.commit()

            # Return data related to the Pizza
            pizza_data = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }

            return jsonify(pizza_data), 201  # HTTP status code 201 for successful creation

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"errors": ["validation errors"]}), 400               

if __name__ == '__main__':
    app.run(port=5555)                   