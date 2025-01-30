from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/get-details")
def get_details():
    return {
        "name": "Vibha",
        "age": 21,
    }

if __name__ == "__main__":
    app.run(port = 3000, debug = True)
