from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS




app = Flask(__name__)
CORS(app)  # You can customize CORS here if needed

app.config.from_object('config')

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
# Initialize the serializer with your app's secret key
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
from app import admin_routes  # Import routes after app is created
# Create tables in the database
with app.app_context():
    db.create_all()