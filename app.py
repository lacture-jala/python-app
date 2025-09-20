from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Home Route"}), 200

@app.route("/api/greet/<string:name>", methods=["GET"])
def greet_user(name):
    return jsonify({"message": f"Hello, {name}!"}), 200

@app.route("/api/square/<int:number>", methods=["GET"])
def calculate_square(number):
    result = number * number
    return jsonify({
        "input": number,
        "operation": "square",
        "result": result
    }), 200

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
