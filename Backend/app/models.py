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
        reset_token (str): Token used for resetting the user's password.
        reset_token_expiration (datetime): Expiration date for the reset token.
        role (str): The role of the user, either 'regular' or 'admin'.
        password (str): The hashed password of the user.
        space_details(SpaceDetails): details for the spaces
        personal_details (PersonalDetails): One-to-one relationship with personal details.
        spaces (List[Spaces]): One-to-many relationship with spaces taken by the user.
    Methods:
        get_id(): Returns the string representation of the user's ID for Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verification = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(120))
    reset_token_expiration = db.Column(db.DateTime)
    role = db.Column(db.String(20), default='regular')  # 'regular' or 'admin'
    password = db.Column(db.String(255), nullable=False)
    personal_details = db.relationship('PersonalDetails', backref='user', uselist=False)
    space_details = db.relationship('SpaceDetails', backref='user', uselist=False)
    spaces = db.relationship('Spaces', backref='user', lazy=True)
    api_key = db.Column(db.String(255), unique=True, nullable=True)  # Store the API key
    space_details_completed = db.Column(db.Boolean, default=False)  # New column



    def get_id(self):
        return str(self.id)  # Convert user ID to string for Flask-Login
# PersonalDetails Model
class PersonalDetails(db.Model):
    """
    Represents personal details associated with a user.
    Attributes:
        id (int): The unique identifier for the personal details.
        first_name(str): the first name of the user
        last_name(str): the last name of the user
        contacts(float): contacts of the user
        gender(str):  gender of the user
        image_url (str): URL to the user's profile image.
       
        national_id (str): The national identification number of the user.
        user_id (int): The ID of the associated user.
    Relationships:
        user (User): The user associated with these personal details.
    """
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    contacts = db.Column(db.Integer(255))
    gender = db.Column(db.String(255))

    resident_type = db.Column(db.String(20))  # 'foreign' or 'Kenyan'
    
    national_id = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# space Model
class Space(db.Model):
    """
    Represents  space taken by a user.
    Attributes:
        id (int): The unique identifier for the space.
        
        amount (float): The amount of the space.
        duration (int): The duration to stay in the space  in months.
        location(str): the location where space is found.
        
        taken_time (datetime): The date and time when the space was taken.
        status (str): The status of the space, default is 'pending'.
        user_id (int): The ID of the user who took the space.
        space_available_id (int): The ID of the available space type this space is based on.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    amount = db.Column(db.Float)
    duration = db.Column(db.Integer)
    location = db.Column(db.String(255))
    taken_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'occupied', 'not_occupied', or 'in progress'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    space_available_id = db.Column(db.Integer, db.ForeignKey('spaces_available.id'), nullable=True)
    # Relationships
    space_available = db.relationship('SpaceAvailable', backref=db.backref('spaces', lazy=True))
    def __repr__(self):
        return (f"Space(id={self.id}, location={self.location}, amount={self.amount}, "
                f"duration={self.duration}, "
                f"taken_time={self.taken_time}, status='{self.status}', "
                f"user_id={self.user_id}, space_available_id={self.space_available_id})")
# SpaceAvailable Model
class SpaceAvailable(db.Model):
    """
    Represents a type of place available for users to request.
    Attributes:
        id (int): The unique identifier for the available space type.
        name (str): The name of the space type.
        space_type (str): The type/category/location of the space.
        amount (float): The maximum amount that can be requested for this space type.
        interest_rate (float): The interest rate for this space type.
        duration_months (int): The maximum duration in months for this space.
    """
    __tablename__ = 'spaces_available'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    space_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return (f"SpaceAvailable(id={self.id}, name='{self.name}', space_type='{self.space_type}', space_location='{self.location}' "
                f"amount={self.amount}, interest_rate={self.interest_rate}, "
                f"duration_months={self.duration_months})")
# payment Model
class Payment(db.Model):
    """
    Represents a payment for the space.
    Attributes:
        id (int): The unique identifier for the payment.
        amount_to_paid (float): The amount paid in this repayment.
        last_payment_date (datetime): The date of the last payment made.
        status (str): The status of the repayment, either 'full' or 'partial'.
        space_id (int): The ID of the space associated with this payment.
    Relationships:
        space (Space): The space associated with this repayment.
    """
    id = db.Column(db.Integer, primary_key=True)
    amount_to_paid = db.Column(db.Float)
    last_payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20)) 
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)