from random import randint, choice as rc

from faker import Faker

from app import app
from Backend.app.models import User, PersonalDetails, Space,  SpaceAvailable, Payment

fake = Faker()

def seed_data():
    # Create sample users
    user1 = User(username='john_doe', email='john@example.com')
    user1.set_password('password')
    user2 = User(username='jane_doe', email='jane@example.com')
    user2.set_password('password')

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create sample spaces
    space1 = Space(name='Maryland', Location='Washington DC', user_id=user1.id)
    space2 = Space(name='Lavington', location='Nairobi', user_id=user2.id)

    # Add events to the session
    db.session.add(space1)
    db.session.add(space2)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        seed_data()  # Seed the database
