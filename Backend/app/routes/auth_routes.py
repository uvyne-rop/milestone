from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, mail
from app.models import User
from app.email_utils import send_verification_email

bp = Blueprint('routes', __name__)

@bp.route('/send_verification_email/<int:user_id>', methods=['GET', 'POST'])
def send_verification_email_route(user_id):
    user = User.query.get_or_404(user_id)
    send_verification_email(user)
    flash('An email has been sent with instructions to verify your email.', 'info')
    return redirect(url_for('routes.home'))

@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
def verify_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('routes.home'))
    user.verification = True
    db.session.commit()
    flash('Your email has been verified!', 'success')
    return redirect(url_for('routes.home'))

@bp.route('/')
def home():
    return 'Home Page'
