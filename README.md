# Project Name
Marketing Expense Logger Backend (API)

## About
This is a Flask-based backend application for the Marketing Expense Logger. The backend provides RESTful API endpoints for user authentication, expense management, and report generation. The application uses MongoDB as the database and integrates with a frontend React app.

## Features
User authentication (login, signup, reset password)
Expense management (add, update, delete, fetch expenses)
Report generation
Secure password handling with bcrypt
JWT-based authentication
Email support for password reset

### Installation
Clone the Repository:
git clone https://github.com/ipcompscience/marketing-expense-logger-backend.git
cd marketing-expense-logger-backend

Install Dependencies:
pip install -r requirements.txt

Start the Development Server:
python app.py

### Technologies Used
**Flask** - A lightweight WSGI web application framework.
**MongoDB** - A NoSQL database for storing user and expense data.
**Flask-PyMongo** - A Flask extension that makes it easy to use MongoDB.
**Flask-JWT-Extended** - A Flask extension for JSON Web Token (JWT) authentication.
**Flask-Mail** - A Flask extension for sending emails.
**Flask-Bcrypt** - A Flask extension for bcrypt hashing.
**itsdangerous** - A Python library for generating secure tokens.

## Contact
If you have any questions or need further assistance, please contact ipcompscience@gmail.com.