from app import app
import random
from models import db, Pizza, Restaurant, RestaurantPizza
from faker import Faker

with app.app_context():

    db.drop_all()
    db.create_all()

    fake = Faker()

    print("🍕 Seeding delicious pizzas...")
    pizzas = [
        {"name": "Mediterranean Delight", "ingredients": "Pizza dough, hummus, cherry tomatoes, black olives, red onion, feta cheese, spinach leaves"},
        {"name": "Spicy Veggie Fusion", "ingredients": "Pizza dough, spicy tomato sauce, bell peppers, jalapeños, red onion, mushrooms, mozzarella cheese"},
        {"name": "Sausage and Artichoke Supreme", "ingredients": "Pizza dough, tomato sauce, Italian sausage, artichoke hearts, red bell peppers, mozzarella cheese"},
        {"name": "Garlic Chicken Alfredo", "ingredients": "Pizza dough, alfredo sauce, garlic chicken, spinach, sun-dried tomatoes, parmesan cheese"},
        {"name": "Pesto Shrimp Delight", "ingredients": "Pizza dough, pesto sauce, shrimp, cherry tomatoes, feta cheese, arugula"},
        {"name": "Bacon Ranch BBQ", "ingredients": "Pizza dough, BBQ sauce, bacon, ranch dressing, red onion, cheddar cheese"},
        {"name": "Truffle Mushroom Feast", "ingredients": "Pizza dough, truffle oil, mixed mushrooms, fontina cheese, arugula"},
        {"name": "Spinach and Artichoke Alfredo", "ingredients": "Pizza dough, alfredo sauce, spinach, artichoke hearts, mozzarella cheese"},
        {"name": "Buffalo Cauliflower Crunch", "ingredients": "Pizza dough, buffalo cauliflower, blue cheese crumbles, celery, ranch drizzle"},
        {"name": "Mexican Street Corn Pizza", "ingredients": "Pizza dough, elote-style corn, cotija cheese, chili powder, lime, cilantro"},
        {"name": "Tandoori Chicken Delight", "ingredients": "Pizza dough, tandoori chicken, curry sauce, bell peppers, red onion, cilantro, yogurt drizzle"},
        {"name": "Seafood Extravaganza", "ingredients": "Pizza dough, marinara sauce, shrimp, scallops, mussels, calamari, garlic, parsley"}
    ]

    for pizza_data in pizzas:
        pizza = Pizza(**pizza_data)
        db.session.add(pizza)

    print("🍽️ Seeding diverse restaurants...")

    restaurants = []

    for i in range(30):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address(),
        )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()

    print("🍕 Adding unique pizzas to restaurants...")

    for pizza in Pizza.query.all():
        for _ in range(random.randint(1, 5)):
            price = random.uniform(5, 25)
            restaurant = Restaurant.query.order_by(db.func.random()).first()
            restaurant_pizzas = RestaurantPizza(pizza_id=pizza.id, restaurant_id=restaurant.id, price=price)
            db.session.add(restaurant_pizzas)

    db.session.commit()
    print("🍕 Done seeding!")