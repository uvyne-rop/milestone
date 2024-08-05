# # app/email_utils.py

# from flask_mail import Message
# from flask import render_template
# from app import mail

# def send_verification_email(user_email, token):
#     msg = Message('Email Verification', recipients=[user_email])
#     msg.body = render_template('verification.txt', token=token)
#     msg.html = render_template('verification.html', token=token)
#     mail.send(msg)
