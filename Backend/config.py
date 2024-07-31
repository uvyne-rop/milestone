from flask import Flask
# from dotenv import load_dotenv
import os
from datetime import timedelta
# from flask_session import Session
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager, decode_token

# Load variables from .env file
# load_dotenv()
app = Flask(__name__)
# Configure the app with variables from the .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_MAX_EMAILS'] = os.getenv('MAIL_MAX_EMAILS')
app.config['MAIL_ASCII_ATTACHMENTS'] = os.getenv('MAIL_ASCII_ATTACHMENTS').lower() == 'true'
# Session Configuration using Filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_NAME'] = 'server_session'  # Customize session cookie name
app.config['SESSION_COOKIE_HTTPONLY'] = False  # Prevents JavaScript from accessing the cookie
app.config['SESSION_COOKIE_SECURE'] = True  # Ensures cookies are sent over HTTPS only
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Prevents CSRF attacks
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Adjust based on your requirements
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory to store uploaded images
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size: 16MB
# AWS S3 Configuration
# app.config['S3_BUCKET_NAME'] = os.getenv('S3_BUCKET_NAME')
# app.config['S3_REGION'] = os.getenv('S3_REGION')
# app.config['S3_ACCESS_KEY'] = os.getenv('AWS_ACCESS_KEY_ID')
# app.config['S3_SECRET_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECTET_KEY')
jwt = JWTManager(app)
# Session(app)