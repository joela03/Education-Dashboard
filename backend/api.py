"""Functions that query the mathnasium database"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def endpoint_index():
    """Sets up index route"""
    return jsonify({"message": "Welcome to the Mathnasium API"})

@app.route("/attendance", methods=["GET", "POST"])
def endpoint_get_movies():
    """Returns students that have attended in a given period"""

    

if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)