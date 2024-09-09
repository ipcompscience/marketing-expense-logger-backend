# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_mail import Mail, Message
from utils.database import mongo
from services.auth import (
    authenticate_user,
    register_user,
    reset_user_password,
    verify_reset_token,
    update_user_password,
)
import os

app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret_key')  # Fallback to a default key if not set
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://dburl/expensesdb')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@example.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-email-password')

CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

# Initialize the database
mongo.init_app(app)


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = authenticate_user(data['email'], data['password'])
    if user:
        access_token = create_access_token(identity={'email': user['email']})
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        register_user(data['email'], data['password'])
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    try:
        reset_user_password(data['email'], mail)  # Pass the mail object to the reset function
        return jsonify({'message': 'Password reset link sent to your email'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/auth/reset-password/<token>', methods=['POST'])
def handle_reset_password(token):
    data = request.json
    email = verify_reset_token(token)
    if not email:
        return jsonify({'message': 'Invalid or expired token'}), 400
    update_user_password(email, data['password'])
    return jsonify({'message': 'Password updated successfully'}), 200


@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = mongo.db.expenses.find()
    return jsonify([expense for expense in expenses]), 200


@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    mongo.db.expenses.insert_one(data)
    return jsonify(data), 201


@app.route('/expenses/<string:id>', methods=['PUT'])
def update_expense(id):
    data = request.json
    mongo.db.expenses.update_one({'_id': id}, {'$set': data})
    return jsonify({'message': 'Expense updated successfully'}), 200


@app.route('/expenses/<string:id>', methods=['DELETE'])
def delete_expense(id):
    mongo.db.expenses.delete_one({'_id': id})
    return jsonify({'message': 'Expense deleted successfully'}), 200


@app.route('/reports', methods=['POST'])
def generate_report():
    filters = request.json
    # Implement report generation logic here
    return jsonify({'message': 'Report generated'}), 200


if __name__ == '__main__':
    app.run(debug=True)
