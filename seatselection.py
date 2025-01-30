from flask import Flask, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Seat model
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    occupied = db.Column(db.Boolean, default=False)

# Define BillingRecord model
class BillingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_index = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)

# Initialize the database and create tables
with app.app_context():
    db.create_all()
    # Initialize seats if not already done
    if Seat.query.count() == 0:
        for _ in range(50):
            db.session.add(Seat())
        db.session.commit()

@app.route("/seats", methods=["GET"])
def get_seats():
    """Return the current status of all seats."""
    seats = Seat.query.all()
    seat_status = [seat.occupied for seat in seats]
    return jsonify({"seats": seat_status})

@app.route("/select-seat", methods=["POST"])
def select_seat():
    """Select a seat by its index and bill the manager."""
    data = request.json
    seat_index = data.get("seat_index")
    user_id = data.get("user_id")  # Assume user ID is provided by the frontend

    if seat_index is None or not isinstance(seat_index, int) or seat_index < 0 or seat_index >= 50:
        return jsonify({"error": "Invalid seat index"}), 400

    seat = Seat.query.get(seat_index)

    if seat.occupied:
        return jsonify({"error": "Seat already occupied"}), 400

    # Mark the seat as occupied
    seat.occupied = True
    db.session.commit()

    # Create a billing record
    billing_record = BillingRecord(
        seat_index=seat_index,
        user_id=user_id,
        amount=10.0,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    db.session.add(billing_record)
    db.session.commit()

    # Return the updated seat list and billing confirmation
    return jsonify({
        "seats": [s.occupied for s in Seat.query.all()],
        "billing_record": {
            "transaction_id": billing_record.id,
            "seat_index": billing_record.seat_index,
            "user_id": billing_record.user_id,
            "amount": billing_record.amount,
            "timestamp": billing_record.timestamp,
        },
    })

@app.route("/billing-history", methods=["GET"])
def get_billing_history():
    """Return the billing history for the manager."""
    records = BillingRecord.query.all()
    billing_history = [{
        "transaction_id": record.id,
        "seat_index": record.seat_index,
        "user_id": record.user_id,
        "amount": record.amount,
        "timestamp": record.timestamp,
    } for record in records]
    
    return jsonify({"billing_history": billing_history})

@app.route("/reset-seats", methods=["POST"])
def reset_seats():
    """Reset all seats to available (for testing purposes)."""
    Seat.query.update({Seat.occupied: False})
    
    # Clear all billing records
    BillingRecord.query.delete()
    
    db.session.commit()
    
    return jsonify({"message": "All seats and billing records reset successfully"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
