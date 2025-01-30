from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize 50 seats (False = available, True = occupied)
seats = [False] * 50

@app.route("/seats", methods=["GET"])
def get_seats():
    """Return the current status of all seats."""
    return jsonify({"seats": seats})

@app.route("/select-seat", methods=["POST"])
def select_seat():
    """Select a seat by its index."""
    data = request.json
    seat_index = data.get("seat_index")

    if seat_index is None or not isinstance(seat_index, int) or seat_index < 0 or seat_index >= 50:
        return jsonify({"error": "Invalid seat index"}), 400

    if seats[seat_index]:
        return jsonify({"error": "Seat already occupied"}), 400

    seats[seat_index] = True  # Mark the seat as occupied
    return jsonify({"seats": seats})  # Return the updated seat list

@app.route("/reset-seats", methods=["POST"])
def reset_seats():
    """Reset all seats to available (for testing purposes)."""
    global seats
    seats = [False] * 50
    return jsonify({"message": "All seats reset successfully"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)