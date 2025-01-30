from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# SQLite setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Regex for IBM email validation
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9_.+-]+@ibm\.com$')

# Database model for Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'employee' or 'manager'
    wallet_money = db.Column(db.Integer, default=1000)  # Default wallet money for each user
    reports_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Who they report to (manager)
    manager = db.relationship('User', remote_side=[id])  # For linking employee and their manager

    def __repr__(self):
        return f'<User {self.name}>'

# Route for Signup
@app.route("/signup_manager", methods=["POST"])
def signup_manager():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")  # You should hash the password in production!


    if not EMAIL_PATTERN.match(email):
        return jsonify({"message": "Invalid email format. Only @ibm.com allowed."}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered."}), 400


    new_user = User(name=name, email=email, role="manager", wallet_money=1000)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful!"}), 201

@app.route("/signup_employee", methods=["POST"])
def signup_employee():
    data = request.get_json()
    name = data.get("name")
    manager_email=data.get("reports_to")
    email = data.get("email")
    password = data.get("password")  # You should hash the password in production!


    if not EMAIL_PATTERN.match(email):
        return jsonify({"message": "Invalid email format. Only @ibm.com allowed."}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already registered."}), 400

    # Create a new user (assuming it's an employee for now)
    new_user = User(name=name, email=email, role="employee", wallet_money=1000)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful!"}), 201

# Route for Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")  # Assume password handling is done via a secure system

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found."}), 404

    # Check if role is manager or employee
    if user.role == "manager":
        return jsonify({
            "message": "Login successful.",
            "role": "manager",
            "wallet_money": user.wallet_money
        })
    elif user.role == "employee":
        manager = User.query.get(user.reports_to) if user.reports_to else None
        return jsonify({
            "message": "Login successful.",
            "role": "employee",
            "wallet_money": user.wallet_money,
            "manager": manager.name if manager else None
        })
    return jsonify({"message": "Invalid role."}), 400

# Route for Booking Seats and Deducting Money
@app.route("/book_seat", methods=["POST"])
def book_seat():
    data = request.get_json()
    employee_id = data.get("employee_id")

    employee = User.query.get(employee_id)
    if not employee:
        return jsonify({"message": "Employee not found."}), 404

    if employee.wallet_money >= 100:
        # Deduct 100 blue dollars from the employee's wallet
        employee.wallet_money -= 100

        # Deduct money from manager's wallet
        if employee.reports_to:
            manager = User.query.get(employee.reports_to)
            if manager:
                manager.wallet_money -= 100

        db.session.commit()
        return jsonify({"message": "Seat booked. Wallet money deducted."})
    else:
        return jsonify({"message": "Not enough wallet money to book a seat."}), 400

# Route to check daily wallet money (For testing)
@app.route("/get_wallet", methods=["GET"])
def get_wallet():
    # Fetch wallet balance for the logged-in user
    email = request.args.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify({
        "email": user.email,
        "role": user.role,
        "wallet_money": user.wallet_money
    })

if __name__ == "__main__":
    # Create the tables before the app runs
    with app.app_context():
        db.create_all()

    # Start the Flask app
    app.run(port=3000, debug=True)
