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
    {"name": "Veggie Supreme", "ingredients": "Pizza dough, tomato sauce, bell peppers, mushrooms, black olives, red onion, mozzarella cheese"},
    {"name": "Spicy Chicken Fiesta", "ingredients": "Pizza dough, spicy tomato sauce, grilled chicken, jalapeños, red peppers, red onion, cheddar cheese"},
    {"name": "Pepperoni Paradise", "ingredients": "Pizza dough, tomato sauce, pepperoni, green peppers, red onion, black olives, mozzarella cheese"},
    {"name": "BBQ Bacon Bliss", "ingredients": "Pizza dough, BBQ sauce, bacon, caramelized onions, mushrooms, mozzarella cheese"},
    {"name": "Margarita Marvel", "ingredients": "Pizza dough, tomato sauce, fresh mozzarella, cherry tomatoes, basil, balsamic glaze"},
    {"name": "Pesto Chicken Delight", "ingredients": "Pizza dough, pesto sauce, grilled chicken, sun-dried tomatoes, artichoke hearts, feta cheese"},
    {"name": "Hawaiian Luau", "ingredients": "Pizza dough, tomato sauce, ham, pineapple, red onion, mozzarella cheese"},
    {"name": "Mushroom Truffle Delight", "ingredients": "Pizza dough, truffle oil, assorted mushrooms, caramelized onions, fontina cheese, arugula"},
    {"name": "Buffalo Chicken Ranch", "ingredients": "Pizza dough, buffalo sauce, grilled chicken, ranch dressing, red onion, celery, blue cheese crumbles"},
    {"name": "Mediterranean Veggie Bliss", "ingredients": "Pizza dough, hummus, cherry tomatoes, kalamata olives, red peppers, red onion, feta cheese, spinach"},
    {"name": "Spinach and Feta Fantasy", "ingredients": "Pizza dough, tomato sauce, spinach, feta cheese, black olives, red onion, garlic"},
    {"name": "Taco Tuesday Pizza", "ingredients": "Pizza dough, seasoned beef, salsa, cheddar cheese, lettuce, tomatoes, sour cream"},
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