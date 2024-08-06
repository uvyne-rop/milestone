from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    """
    Represents a user in the application.
    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        verification (bool): Indicates if the user's email address has been verified.
        role (str): The role of the user, either 'client' or 'admin'.
        password (str): The hashed password of the user.
        spaces (List[Space]): One-to-many relationship with spaces taken by the user.
    Methods:
        get_id(): Returns the string representation of the user's ID for Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='client')  # 'client' or 'admin'
    password = db.Column(db.String(255), nullable=False)

    # One-to-many relationship with spaces and payments
    spaces = db.relationship('Space', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def get_id(self):
        return str(self.id)  # Convert user ID to string for Flask-Login

# ManageUser Model
class ManageUser(db.Model):
    """
    Represents an administrative user responsible for managing spaces.
    Attributes:
        id (int): The unique identifier for the manager.
        first_name (str): The first name of the manager.
        last_name (str): The last name of the manager.
        email (str): The email address of the manager.
        verified (bool): Indicates if the manager's email address has been verified.
        role (str): The role of the manager, typically 'admin'.
        password (str): The hashed password of the manager.
        space_name (str): The name of the space managed by the user.
        location (str): The location of the space managed by the user.
        amount (float): The amount associated with the space.
        date_paid (datetime): The date the last payment was made.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='admin')
    password = db.Column(db.String(255), nullable=False)
    space_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    amount = db.Column(db.Float)
    date_paid = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f"ManageUser(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', "
                f"email='{self.email}', verified={self.verified}, role='{self.role}', "
                f"space_name='{self.space_name}', location='{self.location}', amount={self.amount}, date_paid={self.date_paid})")

# Space Model
class Space(db.Model):
    """
    Represents a space available for rent.
    Attributes:
        id (int): The unique identifier for the space.
        name (str): The name of the space.
        location (str): The location where the space is found.
        description (str): A detailed description of the space.
        rating (float): The rating of the space.
        status (str): The status of the space, can be 'Booked' or 'Free'.
        imageUrl (str): The URL of the image associated with the space.
        user_id (int): The ID of the user who took the space.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='Free')  # 'Booked' or 'Free'
    imageUrl = db.Column(db.String(255), nullable=True)  # New attribute for image URL
    role = db.Column(db.String(20), default='admin')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return (f"Space(id={self.id}, name='{self.name}', location='{self.location}', "
                f"description='{self.description}', rating={self.rating}, status='{self.status}', "
                f"imageUrl='{self.imageUrl}')")


# Payment Model
class Payment(db.Model):
    """
    Represents a payment for the space.
    Attributes:
        id (int): The unique identifier for the payment.
        user_id (int): The ID of the user who made the payment.
        amount (float): The amount paid.
        date_paid (datetime): The date the payment was made.
        space_id (int): The ID of the space associated with this payment.
        first_name (str): The first name of the user who made the payment.
        last_name (str): The last name of the user who made the payment.
        contacts (str): The contact details of the user who made the payment.
        payment_mode (str): The mode of payment used.
        message (str): Additional message or note related to the payment.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price in KSH
    rating = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(10), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # bookings = db.relationship('BookedSpace', backref='space', lazy=True)
    # reviews = db.relationship('Review', backref='space', lazy=True)

    def __repr__(self):
        return (f"Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, date_paid={self.date_paid}, "
                f"space_id={self.space_id}, first_name='{self.first_name}', last_name='{self.last_name}', "
                f"contacts='{self.contacts}', payment_mode='{self.payment_mode}', message='{self.message}')")

# Review Model
class Review(db.Model):
    """
    Represents a review for a space.
    Attributes:
        id (int): The unique identifier for the review.
        user_id (int): The ID of the user who wrote the review.
        space_id (int): The ID of the space being reviewed.
        review_message (str): The content of the review message.
        rating (int): The rating given by the user in stars.
        user_first_name (str): The first name of the user who wrote the review.
        user_last_name (str): The last name of the user who wrote the review.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)
    review_message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating in stars
    user_first_name = db.Column(db.String(50), nullable=False)
    user_last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return (f"Review(id={self.id}, user_id={self.user_id}, space_id={self.space_id}, "
                f"review_message='{self.review_message}', rating={self.rating}, "
                f"user_first_name='{self.user_first_name}', user_last_name='{self.user_last_name}')")

# BookedSpace Model
class BookedSpace(db.Model):
    """
    Represents a booked space by a user.
    Attributes:
        id (int): The unique identifier for the booked space.
        user_id (int): The ID of the user who booked the space.
        space_id (int): The ID of the space that has been booked.
        user_first_name (str): The first name of the user who booked the space.
        user_last_name (str): The last name of the user who booked the space.
        email (str): The email address of the user who booked the space.
        contact (str): The contact details of the user.
        space_name (str): The name of the space booked.
        location (str): The location of the space.
        image_url (str): The URL of the image representing the space.
        status (str): The booking status of the space, either 'Booked' or 'Free'.
        paid (bool): Indicates whether the payment has been made.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)
    user_first_name = db.Column(db.String(50), nullable=False)
    user_last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    space_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False)  # 'Booked' or 'Free'
    paid = db.Column(db.Boolean, default=False)  # Indicates payment status

    def __repr__(self):
        return (f"BookedSpace(id={self.id}, user_id={self.user_id}, space_id={self.space_id}, "
                f"user_first_name='{self.user_first_name}', user_last_name='{self.user_last_name}', "
                f"email='{self.email}', contact='{self.contact}', space_name='{self.space_name}', "
                f"location='{self.location}', image_url='{self.image_url}', status='{self.status}', "
                f"paid={self.paid})")
