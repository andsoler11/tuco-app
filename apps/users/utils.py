from django.contrib import messages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from utils.privacy import Privacy
from django.core.cache import cache
import secrets

privacy = Privacy()

def generate_reset_token():
    reset_token = secrets.token_urlsafe(32)
    return reset_token

def send_recovery_email(request, user_email):
    fail = False
    subject = 'Recuperación de contraseña Foreverdog'
    reset_token = generate_reset_token()

    message = f'Dale click al siguiente enlace para recuperar tu contraseña : {request.build_absolute_uri("/new-password-token/")}?token={reset_token}'
    from_email = settings.EMAIL_HOST_USER
    to_email = user_email

    # Create the email message
    email = MIMEMultipart()
    email['From'] = from_email
    email['To'] = to_email
    email['Subject'] = subject

    # Attach the message to the email
    email.attach(MIMEText(message, 'plain'))
    try:
        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server details
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_PASSWORD)  # Replace with your email login credentials
        smtp_server.send_message(email)
        smtp_server.quit()
        cache.set(reset_token, user_email, 3600)
    except Exception as e:
        print(f'Error sending email: {e}')
        fail = True

    return fail


def validate_password(request, password):
    # Define the minimum requirements for a secure password
    min_length = 8
    min_numeric = 1
    min_special_chars = 1
    passed = True

    # Check password length
    if len(password) < min_length:
        messages.error(request, f"La contraseña debe tener al menos {min_length} caracteres.")
        passed = False

    # Check for at least one numeric character
    if sum(char.isdigit() for char in password) < min_numeric:
        messages.error(request, f"La contraseña debe contener al menos {min_numeric} número(s).")
        passed = False

    # Check for at least one special character
    special_chars = "!@#$%^&*()_-=+[]{};:,.<>/?"
    if sum(char in special_chars for char in password) < min_special_chars:
        messages.error(request, f"La contraseña debe contener al menos {min_special_chars} caracter(es) especial(es).")
        passed = False

    return passed
