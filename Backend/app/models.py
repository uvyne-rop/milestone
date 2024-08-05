from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verification = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(120))
    reset_token_expiration = db.Column(db.DateTime)
    role = db.Column(db.String(20), default='regular')
    password = db.Column(db.String(255), nullable=False)
    personal_details = db.relationship('PersonalDetails', backref='user', uselist=False, foreign_keys='PersonalDetails.user_id')
    spaces = db.relationship('Space', backref='user', lazy=True)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    space_details_completed = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

class PersonalDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    contacts = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(255))
    resident_type = db.Column(db.String(20))
    national_id = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    amount = db.Column(db.Float)
    duration = db.Column(db.Integer)
    location = db.Column(db.String(255))
    taken_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    space_available_id = db.Column(db.Integer, db.ForeignKey('spaces_available.id'), nullable=True)
    space_available = db.relationship('SpaceAvailable', backref=db.backref('spaces', lazy=True))

    def __repr__(self):
        return (f"Space(id={self.id}, location={self.location}, amount={self.amount}, "
                f"duration={self.duration}, taken_time={self.taken_time}, status='{self.status}', "
                f"user_id={self.user_id}, space_available_id={self.space_available_id})")

class SpaceAvailable(db.Model):
    __tablename__ = 'spaces_available'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    space_type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (f"SpaceAvailable(id={self.id}, name='{self.name}', space_type='{self.space_type}', location='{self.location}' "
                f"amount={self.amount}, interest_rate={self.interest_rate}, duration_months={self.duration_months})")

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_to_paid = db.Column(db.Float)
    last_payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)
