# services/auth.py
from flask_bcrypt import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from utils.database import mongo

s = URLSafeTimedSerializer('your_secret_key')  # Use the same secret key as your app

def authenticate_user(email, password):
    user = mongo.db.users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return user
    return None

def register_user(email, password):
    if mongo.db.users.find_one({'email': email}):
        raise Exception('User already exists')
    hashed_password = generate_password_hash(password).decode('utf-8')
    mongo.db.users.insert_one({'email': email, 'password': hashed_password})

def reset_user_password(email):
    user = mongo.db.users.find_one({'email': email})
    if not user:
        raise Exception('User not found')
    
    # Generate a secure token
    token = s.dumps(email, salt='password-reset-salt')

    # Send the password reset email
    msg = Message('Password Reset Request',
                  sender='noreply@example.com',
                  recipients=[email])
    reset_link = f'https://ipexpenseloggertest.com/auth/reset-password/{token}'
    msg.body = f'Please use the following link to reset your password: {reset_link}'
    mail.send(msg)

def verify_reset_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires in 1 hour
        return email
    except:
        return None

def update_user_password(email, new_password):
    hashed_password = generate_password_hash(new_password).decode('utf-8')
    mongo.db.users.update_one({'email': email}, {'$set': {'password': hashed_password}})
