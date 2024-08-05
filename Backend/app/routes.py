# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from app.email_utils import send_verification_email
from itsdangerous import URLSafeTimedSerializer
from app import db
from app.models import User

bp = Blueprint('routes', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        user = User(email=email)
        db.session.add(user)
        db.session.commit()
        
        # Generate a token for email verification
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(user.email, salt='email-confirm-salt')
        
        # Send verification email
        send_verification_email(user.email, token)
        
        return redirect(url_for('routes.home'))
    
    return render_template('register.html')

@bp.route('/verify_email/<token>')
def verify_email(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='email-confirm-salt', max_age=3600)
        user = User.query.filter_by(email=email).first_or_404()
        user.email_verified = True
        db.session.commit()
        return redirect(url_for('routes.home'))
    except Exception as e:
        return str(e)  # In production, you might want to render an error template
