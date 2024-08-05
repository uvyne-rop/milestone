import secrets
from flask import Flask, render_template, request, redirect, url_for, flash,json, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from flask import abort
from app.models import db, User, PersonalDetails, Space,  SpaceAvailable, Payment
from config import app
from datetime import datetime, timedelta  # Import datetime module
from dateutil.relativedelta import relativedelta
from flask_session import Session
from sqlalchemy.exc import IntegrityError  # Import IntegrityError from SQLAlchemy
import os
import boto3
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from functools import wraps
from sqlalchemy.orm.exc import NoResultFound
from flask_migrate import Migrate
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from config import app
from flask_cors import CORS


CORS(app)  # You can customize CORS here if needed

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = secrets.token_hex(16)


users = {
    "admin_user": {"role": "admin"},
    "regular_user": {"role": "user"}
}

# Custom admin_required decorator
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Ensure the request has a valid JWT token
            user_id = get_jwt_identity()  # Get the identity of the current user
            user = users.get(user_id, None)
            
            if user and user.get("role") == "admin":
                return fn(*args, **kwargs)
            else:
                return jsonify({"error": "Admin access required"}), 403

        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return wrapper


# Initialize the serializer with  app's secret key
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 #Initialize S3 client
# s3_client = boto3.client(
#     's3',
#     region_name=app.config['S3_REGION'],
#     aws_access_key_id=app.config['S3_ACCESS_KEY'],
#     aws_secret_access_key=app.config['S3_SECRET_KEY']
#)
# # Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
mail = Mail(app)
# db.init_app(app)
login_manager = LoginManager(app)
app.config.from_object('config')  #  space configuration from config.py
# Initialize Flask-Session
Session(app)
# Create tables in the database
with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Decorator for admin-only routes
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.role != 'admin':
#             return jsonify({"message": "Access denied, admin only"}), 403
#         return f(*args, **kwargs)
#     return decorated_function
# def generate_api_key():
#     import uuid
#     return str(uuid.uuid4())
# def store_api_key(user_id):
#     api_key = generate_api_key()
#     user = User.query.get(user_id)
#     user.api_key = api_key
#     db.session.commit()
#     return api_key
# def require_api_key(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         api_key = request.headers.get('x-api-key') or request.args.get('api_key')
        
#         if not api_key or not User.query.filter_by(api_key=api_key).first():
#             return jsonify({"message": "Invalid or missing API key"}), 401
        
    #     return f(*args, **kwargs)
    
    # return decorated_function
#Assuming `serializer` is initialized elsewhere with your app's secret key
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
# Function to generate confirmation token
def generate_confirmation_token(email):
    return serializer.dumps(email, salt='email-confirm')
# Function to send email confirmation
def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    
    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Email Verification</title>
      <style>
        /* Reset styles for email clients */
        body, html {{
          font-family: Arial, sans-serif;
          line-height: 1.6;
          margin: 0;
          padding: 0;
        }}
        /* Container styles */
        .container {{
          max-width: 600px;
          margin: 20px auto;
          padding: 20px;
          background-color: #f9f9f9;
          border-radius: 8px;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        /* Heading styles */
        h2 {{
          color: #333;
          text-align: center;
          margin-bottom: 20px;
        }}
        /* Button styles */
        .btn {{
          display: inline-block;
          padding: 10px 20px;
          background-color: #007bff;
          color: #fff;
          text-decoration: none;
          border-radius: 5px;
          text-align: center;
        }}
        /* Paragraph styles */
        p {{
          color: #666;
          font-size: 16px;
          line-height: 1.8;
          margin-bottom: 10px;
        }}
        /* Footer styles */
        .footer {{
          margin-top: 20px;
          text-align: center;
          color: #999;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Email Verification</h2>
        <p>Hi {user.first_name} {user.last_name},</p>
        <p>Please click the button below to verify your email address:</p>
        <a class="btn" href="{confirm_url}">Verify Email</a>
        <p style="margin-top: 20px;">If you didn't request this, please ignore this email.</p>
        <p class="footer">This email was sent to {user.email} from The Groove. </p>
        <p class="footer">Please do not reply to this email.</p>
      </div>
    </body>
    </html>
    """
    msg = Message('Kindly Confirm Your Email Address', 
                  sender=("The Groove", app.config['MAIL_DEFAULT_SENDER']), 
                  recipients=[user.email])
    
    msg.html = html_body
    mail.send(msg)
@app.route('/user/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    # Extract common fields
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    if not first_name or not last_name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400
    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered. Choose another email."}), 400
    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)
  # Generate a new API key
    # api_key = generate_api_key()
    #Create a new user
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        verification=0,
        reset_token=None,
        reset_token_expiration=None,
        role='regular',
        password=hashed_password,  # Store hashed password
        api_key=None  # Initialize API key as None initially
    )
    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()
    # Send email confirmation
    send_confirmation_email(new_user)
    # Redirect or return response indicating successful registration
    return jsonify(
        {
            "message": "Registration successful. Please check your email to confirm your account."
        }
    ), 201
# For GET request, return the registration form (if applicable)
#resend confirmation email
@app.route('/resend_confirmation_email', methods=['POST'])
# @require_api_key
@login_required
def resend_confirmation_email():
    if current_user.verification:
        return jsonify({"message": "Your email is already verified."}), 200
    # Send new confirmation email
    send_confirmation_email(current_user)
    return jsonify({"message": "Confirmation email resent. Please check your email to confirm your account."}), 200

@app.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    try:
        # Decrypt the token to get the email
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # Token expires after 1 hour
        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if user:
            if user.verification:
                flash('Your email is already verified.', 'info')
                return render_template('already_verified.html')
            
            # Set user verification to True
            user.verification = True
            # user.api_key = generate_api_key()  # Generate API key
            db.session.commit()
            # Send API key email to the user
            # send_api_key_email(user, user.api_key)
            flash('Your email has been successfully verified. Please log in.', 'success')
            return render_template('login.html')
            #Redirect to login page
            # return render_template('login.html')  # Adjust 'login' to your actual login route
        else:
            flash('The verification link is invalid or has expired.', 'error')
    #         return render_template('email/invalid_token.html')
    except SignatureExpired:
        return render_template('expired_token.html')
    except BadSignature:
        return render_template('invalid_token.html')
    except Exception as e:
        return render_template('error.html', error=str(e))
# Registration route for admin users
@app.route('/admin/register_admin', methods=['POST'])
def register_admin():
    if request.is_json:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
    else:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
    # Validate required fields
    if not first_name or not last_name or not email or not password:
        response = {
            "message": "All fields are required."
        }
        return jsonify(response), 400
    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        response = {
            "message": "Email already registered. Choose another email."
        }
        return jsonify(response), 409
    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password)
    # Generate a unique API key for the user
    # api_key = generate_api_key()
    # Create a new admin user
    new_admin_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        verification=True,
        reset_token=None,
        reset_token_expiration=None,
        role='admin',
        password=hashed_password,
        # api_key=api_key 
    )
    # Add the admin user to the database
    db.session.add(new_admin_user)
    db.session.commit()
    # Return a success message with status code 201 (Created)
    response = {
        "message": "Admin registration successful. You can now log in.",
        # "api_key": api_key
    }
    return jsonify(response), 201
# If method is not POST, Flask will automatically return a 405 Method Not Allowed
# Landing page route
# @require_api_key



@app.route('/')
@app.route('/<page>')
def serve_page(page=None):
    if page is None or page == 'index':
        return render_template('index.html')
    elif page == 'user_routes':
        return render_template('user_routes.html')
    elif page == 'admin_routes':
        return render_template('admin_routes.html')
    elif page == 'authorization_routes':
        return render_template('authorization_routes.html')
    else:
        return jsonify({"message":"Page Not Found"}), 404
# Universal login route
@app.route('/universal/login', methods=['POST'])
# @require_api_key
def login():
    try:
        # Extract data from the request, handling both form data and JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        # Debugging: Check the content type and what data was received
        # Retrieve email and password from the data
        email = data.get('email')
        password = data.get('password')
        # Validate that email and password are provided
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        # Retrieve the user from the database
        user = User.query.filter_by(email=email).first()
        # Check if user exists and password matches
        if user and check_password_hash(user.password, password):
            if user.verification:  # User is verified
                try:
                    login_user(user)
                    session.permanent = True
                    return jsonify({"message": "Login successful", "user_id": user.id}), 200
                except Exception as e:
                    return jsonify({"message": "Login failed due to an internal error"}), 500
            else:  # User exists and credentials are correct but not verified
                return jsonify({
                    "message": "Your account is not verified. Please check your email for the verification link or resend the verification.",
                    "action": "resend_verification",
                    "user_id": user.id
                }), 403
        else:
            # Invalid credentials response
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        # General error handling with detailed log
        return jsonify({"message": "An error occurred during login", "error": str(e)}), 500
    
@app.route('/logout', methods=['POST'])
# @require_api_key
@login_required
def logout():
    try:
        data = request.form if request.form else request.get_json()
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to logout: {str(e)}"}), 500
@app.route('/user/spacerequest', methods=['POST'])
#@require_api_key
@login_required
def request_spaces():
    """
    Endpoint for users to request a new space.,
    """
    try:
        data = request.get_json()
        # Extract data from the request
        space_name = data.get('space_name')
        amount = data.get('amount')
        duration = data.get('duration')
        # purpose = data.get('purpose')
        #room_available_id =data.get('room_available_id ')
        # Validate input data
        if not all([space_name, amount, duration, ]):
            return jsonify({"message": "All fields are required"}), 400
        # Fetch the specified available spaces
        available_space = SpaceAvailable.query.filter_by(name=space_name).first()
        if not available_space:
            return jsonify({"message": "Requested room is already occupied"}), 400
        # Validate the requested space parameters against the available space
        if amount < available_space.amount or duration > available_space.duration_months:
            return jsonify({
                "message": "Requested rent amount is below or duration exceeds the available  parameters"
            }), 400
        # Create a new place  for the request
        new_space = Space(
            name=space_name,
            amount=amount,
            duration=duration,
            taken_time=datetime.utcnow(),
            status='pending',  # Initial status
            user_id=current_user.id,
            # space_available_id=space_available_id 
             # Assuming current_user is the logged-in user
            space_available_id=available_space.id  # Link to the available space type
        )
        # Add and commit the new space request to the database
        db.session.add(new_space)
        db.session.commit()
        return jsonify({"message": "Space request submitted successfully", "space_id": new_space.id}), 201
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"message": f"Failed to request space: {str(e)}"}), 500
# Route to fetch and display available spaces
@app.route('/universal/spacesavailable', methods=['GET'])
# @require_api_key
@login_required
def get_available_spaces():
    try:
        available_spaces = SpaceAvailable.query.all()
        # Prepare JSON response
        spaces = [
            {
                "id": space.id,
                "name": space.name,
                "space_type":space.space_type,
                "amount": space.amount,
                "interest_rate": space.interest_rate,
                "duration_months": space.duration_months
            }
            for space in available_spaces
        ]
        return jsonify({"available spaces": spaces}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to fetch available spaces: {str(e)}"}), 500
#managing loans
@app.route('/admin/managespaces', methods=['POST', 'DELETE', 'PUT'])
# @require_api_key
@admin_required 
def manage_available_spaces():
    if request.method == 'POST':
        # Add a new space
        data = request.json
        
        if not data:
            return jsonify({"message": "No data received"}), 400
        # Validate input data
        required_fields = ['name', 'space_type', 'amount', 'duration_months']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Field '{field}' is missing"}), 400
        new_space = SpaceAvailable(
            name=data['name'],
            space_type=data['space_type'],
            amount=data['amount'],
          
            duration_months=data['duration_months']
        )
        try:
            db.session.add(new_space)
            db.session.commit()
            return jsonify({"message": "space added successfully"}), 201
        except IntegrityError as e:
            db.session.rollback()
            # Check if the error is due to unique constraint on 'name'
            if 'unique constraint' in str(e.orig):
                return jsonify({"message": "Space with that name already exists"}), 400
            else:
                return jsonify({"message": "Integrity error occurred"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to add space: {str(e)}"}), 500
    
    elif request.method == 'DELETE':
        # Deleting a space by its ID
        data = request.json
        space_id = data.get('id')
        if not space_id:
            return jsonify({"message": "Space ID is required for deletion"}), 400
        space = SpaceAvailable.query.get(space_id)
        if not space:
            return jsonify({"message": "Space not found"}), 404
        try:
            db.session.delete(space)
            db.session.commit()
            return jsonify({"message": "Space deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to delete space: {str(e)}"}), 500
    
    elif request.method == 'PUT':
        # Update an existing space
        data = request.space
        
        if not data:
            return jsonify({"message": "No data received"}), 400
        space_id = data.get('id')
        if not space_id:
            return jsonify({"message": "space ID is required for updating"}), 400
        space = SpaceAvailable.query.get(space_id)
        if not space:
            return jsonify({"message": "space not found"}), 404
        # Update space fields if provided
        space.name = data.get('name', space.name)
        space.space_type = data.get('space_type', space.space_type)
        space.amount = data.get('amount', space.amount)
        # space.interest_rate = data.get('interest_rate', space.interest_rate)
        space.duration_months = data.get('duration_months', space.duration_months)
        try:
            db.session.commit()
            return jsonify({"message": "Space updated successfully"}), 200
        except IntegrityError as e:
            db.session.rollback()
            if 'unique constraint' in str(e.orig):
                return jsonify({"message": "Space with that name already exists"}), 400
            else:
                return jsonify({"message": "Integrity error occurred"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Failed to update space: {str(e)}"}), 500
    else:
        return jsonify({"message": "Method not allowed"}), 405
# Route for CRUD operations on personal details and images
@app.route('/personal_details', methods=['GET', 'POST', 'PUT', 'DELETE'])
# @require_api_key
@login_required
def manage_personal_details():
    user_id = current_user.id
    personal_details = PersonalDetails.query.filter_by(user_id=user_id).first()
    if request.method == 'GET':
        if personal_details:
            return jsonify({
                
                'first_name': personal_details.first_name,
                'last_name': personal_details.last_name,
                'contacts': personal_details.contacts,
                'gender': personal_details.gender,
                'national_id': personal_details.national_id,
                'image_url': personal_details.image_url
            }), 200
        else:
            return jsonify({'message': 'No personal details found'}), 404
    if request.method == 'POST':
        # Create new personal details
        if personal_details:
            return jsonify({'message': 'Personal details already exist. Use PUT to update.'}), 400
        try:
            if request.content_type == 'multipart/form-data':
                # Handle form data
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                contacts = request.fom.get('contacts')
                gender = request.form.get('gender')
                national_id = request.form.get('national_id')
                # Handle image upload
                image_url = None
                if 'image' in request.files:
                    image = request.files['image']
                    if image.filename != '':
                        filename = secure_filename(image.filename)
                        # s3_client.upload_fileobj(image, app.config['S3_BUCKET_NAME'], filename)
                        image_url = f"https://{app.config['S3_BUCKET_NAME']}.s3.amazonaws.com/{filename}"
            elif request.content_type == 'application/json':
                # Handle JSON data
                data = request.get_json()
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                contacts = data.get('contacts')
                gender = data.get('gender')
                national_id = data.get('national_id')
                # Handle image upload (if applicable)
                image_url = data.get('image_url')
            else:
                return jsonify({'message': 'Unsupported content type'}), 415
            new_details = PersonalDetails(
               first_name=first_name,
               last_name=last_name,
               contacts=contacts,
               gender=gender,
               national_id=national_id,
               image_url=image_url,
               user_id=user_id
            )
            db.session.add(new_details)
            db.session.commit()
            return jsonify({'message': 'Personal details created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Failed to create personal details: {str(e)}'}), 500
    if request.method == 'PUT':
        # Update existing personal details
        if not personal_details:
            return jsonify({'message': 'Personal details not found. Use POST to create new details.'}), 404
        try:
            if request.content_type == 'multipart/form-data':
                # Handle form data update
                personal_details.first_name = request.form.get('first_name', personal_details.first_name)
                personal_details.last_name = request.form.get('last_name', personal_details.last_name)
                personal_details.contacts = request.form.get('contacts', personal_details.contacts)
                personal_details.gender = request.form.get('gender', personal_details.gender)
                personal_details.national_id = request.form.get('national_id', personal_details.national_id)
                # Handle image upload update
                if 'image' in request.files:
                    image = request.files['image']
                    if image.filename != '':
                        filename = secure_filename(image.filename)
                        # s3_client.upload_fileobj(image, app.config['S3_BUCKET_NAME'], filename)
                        personal_details.image_url = f"https://{app.config['S3_BUCKET_NAME']}.s3.amazonaws.com/{filename}"
            elif request.content_type == 'application/json':
                # Handle JSON data update
                data = request.get_json()
                personal_details.first_name = data.get('first_name', personal_details.first_name)
                personal_details.last_name = data.get('last_name', personal_details.last_name)
                personal_details.contacts = float(data.get('contacts', personal_details.contacts))
                personal_details.national_id = data.get('national_id', personal_details.national_id)
                personal_details.image_url = data.get('image_url', personal_details.image_url)
            else:
                return jsonify({'message': 'Unsupported content type'}), 415
            db.session.commit()
            return jsonify({'message': 'Personal details updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Failed to update personal details: {str(e)}'}), 500
    if request.method == 'DELETE':
        # Delete image_url only
        if not personal_details:
            return jsonify({'message': 'Personal details not found.'}), 404
        try:
            personal_details.image_url = None
            db.session.commit()
            return jsonify({'message': 'Image URL deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Failed to delete image URL: {str(e)}'}), 500
    return jsonify({'message': 'Invalid request method'}), 405

# Route for password reset page
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
# @require_api_key
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset-password',
                                 max_age=3600)  # Token expires after 1 hour (3600 seconds)
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            if new_password == confirm_password:
                # Update the user's password
                user = User.query.filter_by(email=email).first()
                if user:
                    user.password = generate_password_hash(new_password)
                    db.session.commit()
                    flash('Password reset successfully. You can now log in with your new password.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('No user found with that email address.', 'error')
            else:
                flash('Passwords do not match.', 'error')
    except:
        flash('Invalid or expired token.', 'error')
    return render_template('user/reset_password.html', token=token)
# occupied and not occupied spaces
@app.route('/admin/space/<int:space_id>/action', methods=['POST'])
# @require_api_key
@admin_required 
def space_action(space_id):
    """
    Endpoint for the admin to assign a space.
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    data = request.get_json()
    action = data.get('action')
    space = None
    try:
        # Retrieve the space using the provided space_id
        space = space.query.filter_by(id=space_id).one()
    except NoResultFound:
        return jsonify({'error': 'Space not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve space: {str(e)}'}), 500
    if action not in ['not_occupied', 'occupied']:
        return jsonify({'error': 'Invalid action'}), 400
    # Check if the name in Space matches the name in SpaceAvailable
    space_available = SpaceAvailable.query.filter_by(name=space.name).first()
    
    if not space_available:
        return jsonify({'error': 'Requested space type is not available'}), 400
    if action == 'not_occupied':
       
        # interest_rate = space_available.interest_rate / 100
        # duration_months = space.space_duration
        # Formula for the total amount to be repaid: A = P(1 + rt)
        total_amount = space.amount 
        # Update the space status to 'occupied' and set space_available_id to None
        space.status = 'not_occupied'
        space.space_available_id = None  # As per the requirement, set this to None after approval
    # Create a new Repayment entry for the space
        new_repayment = Payment(
            amount_to_paid=total_amount,
            last_payment_date=None,  # No payment has been made yet
            status='not paid',
            space_id=space.id
        )
        db.session.add(new_repayment)
        try:
            db.session.commit()
            return jsonify({
                'message': 'Space paid successfully',
                'space_status': space.status,
                'total_repayment_amount': total_amount
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to approve the space: {str(e)}'}), 500
  
    elif action == 'occupied':
        space.status = 'occupied'
        try:
            db.session.commit()
            return jsonify({'message': 'Space already occupied ', 'space_status': space.status}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to occupy the space: {str(e)}'}), 500
#fetching the spaces
@app.route('/admin/getspaces', methods=['GET'])
# @require_api_key
# @admin_required  # Ensure only authenticated users can access this route
def get_space_by_status():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized access'}), 403
    try:
        not_occupied_spaces = Space.query.filter_by(status='not_occupied').all()
        occupied_spaces = Space.query.filter_by(status='occupied_spaces').all()
        
        spaces_data = {
           
            'occupied_spaces': [{
                'id': space.id,
                'first_name': space.first_name,
                'last_name': space.last_name,
                'contacts': space.contacts,
                'gender': space.gender,
                'amount': space.amount,
                'duration': space.duration,
                
                'user_id': space.user_id
                # Add more fields as needed
            } for space in occupied_spaces],
            'not_occupied_spaces': [{
                'id': space.id,
                'amount': space.amount,
                
            } for space in not_occupied_spaces]
        }
        return jsonify(space_data), 200
    except Exception as e:
        return jsonify({"message": f"Failed to fetch spaces: {str(e)}"}), 500
# CRUD Operations for Users by admin
# Create User
@app.route('/admin/users', methods=['POST', 'GET'])
# @require_api_key
@admin_required
def manage_users():
    if request.method == 'POST':
        # Create a new user
        data = request.json
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            role=data.get('role', 'regular')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    elif request.method == 'GET':
        # Retrieve all users
        users = User.query.all()
        users_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role,
                "verification" :user.verification
            } for user in users
        ]
        return jsonify(users_data)
    # Handle unsupported methods if any
    return jsonify({"message": "Method not allowed"}), 405
# Update or Delete User
@app.route('/admin/users/<int:user_id>', methods=['PUT', 'DELETE'])
# @require_api_key
@admin_required
def manage_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User does not exist in the system"}), 404
    if request.method == 'PUT':
        # Update user details
        data = request.json
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        # Optionally update password if provided
        password = data.get('password')
        if password:
            user.password = generate_password_hash(password)
        # Allow admin to update the verification status
        verification_status = data.get('verification')
        if verification_status is not None:
            # Ensure it's a boolean value
            user.verification = bool(verification_status)
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    elif request.method == 'DELETE':
        # Delete user
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    # Handle unsupported methods if any
    return jsonify({"message": "Method not allowed"}), 405
#DASHBOARD ROUTE
@app.route('/user/dashboard', methods=['GET'])
# @require_api_key
@login_required  
def dashboard():
    
    if not current_user.is_authenticated:
        return jsonify({"message": "Unauthorized"}), 401
    # Gather user details
    user_details = {
        "First Name": current_user.first_name,
        "Last Name": current_user.last_name,
        "email": current_user.email,
    }
    user_personal_details=PersonalDetails.query.filter_by(user_id=current_user.id).all()
    details =[
        {"image_url":image.image_url}
        for image in user_personal_details
          ]
    # Gather spaces related to the user
    user_spaces = Space.query.filter_by(user_id=current_user.id).all()
    space_info = [
        {
            "amount": space.amount,
            "duration": space.duration,
            
            "taken_time": space.taken_time,
            "status": space.status,
            "remaining_amount": space.amount - calculate_amount_paid(space.id),  # Assuming a function to calculate paid amount
            "deadline": calculate_space_deadline(space.taken_time, space.duration)  # Assuming a function to calculate deadline
        } for space in user_spaces
    ]
    available_spaces = SpaceAvailable.query.all()
        # Prepare JSON response
    spaces = [
            {
                "id": space.id,
                "name": space.name,
                "space_type":space.space_type,
                "amount": space.amount,
                "interest_rate": space.interest_rate,
                "duration_months": space.duration_months
            }
            for space in available_spaces
        ]
    return jsonify({
        "user_details": user_details,
        "profile_image_url": details,
        "user_spaces": spaces_info,
        "available_spaces": spaces
    })
@app.route('/admin/dashboard', methods=['GET'])
# @require_api_key
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403  # Return 403 Forbidden if not admin
    # Fetch all users excluding sensitive information
    users = User.query.all()
    users_data = []
    for user in users:
        # Fetch associated loans for each user
        user_spaces = Space.query.filter_by(user_id=user.id).all()
        user_spaces_data = []
        for user_space in user_spaces:
            space = Space.query.get(user_space.space_id)
            if space:
                user_space_data.append({
                    "id": space.id,
                    "name": space.name,
                    "amount": space.amount,
                    "status": space.status,
                    
                })
        users_data.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            
            "spaces": user_spaces_data,
            "verification":user.verification
            # Add more properties as needed
        })
    # Fetch all spaces (occupied , not_occupied)
    spaces = Space.query.all()
    spaces_data = []
    for space in spaces:
        spaces_data.append({
            "id": space.id,
            "name": space.name,
            "amount": space.amount,
            "status": space.status,
            # Add more properties as needed
        })
    # Fetch all available spaces
    available_spaces = SpaceAvailable.query.all()
    available_spaces_data = []
    for available_space in available_spaces:
        available_spaces_data.append({
            "id": available_space.id,
            "name": available_space.name,
            "amount": available_space.amount,
            "duration_months": available_spaces.duration_months,
            # Add more properties as needed
        })
    # Prepare JSON response
    response_data = {
        "users": users_data,
        "spaces": spaces_data,
        "available_spaces": available_spaces_data
    }
    return jsonify(response_data)
def calculate_amount_paid(space_id):
    # Replace with actual logic to calculate paid amount
    return 0
def calculate_space_deadline(taken_time, duration):
    # Calculate the deadline by adding the duration in months
    deadline = taken_time + relativedelta(months=duration)
    return deadline
if __name__ == "__main__":
     app.run(host='127.0.0.1', port=8080, debug=True)
