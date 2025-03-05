from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)

# 🔹 Secret key for JWT encryption
app.config["JWT_SECRET_KEY"] = "your_secret_key_here"  # Change this to a strong secret
jwt = JWTManager(app)

# Dummy users (Replace with database users)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "userpass", "role": "user"},
}

# 🔹 Login Endpoint - Generate JWT Token
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in USERS and USERS[username]["password"] == password:
        access_token = create_access_token(identity=username, additional_claims={"role": USERS[username]["role"]})
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# 🔹 Protected API Route (Requires Login)
@app.route("/api/data", methods=["GET"])
@jwt_required()
def get_data():
    current_user = get_jwt_identity()  # Get logged-in username
    return jsonify({"message": f"Hello {current_user}, you have access!", "data": ["item1", "item2", "item3"]})

# 🔹 Admin-Only API Route
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin_route():
    jwt_data = get_jwt()  # Get JWT claims
    role = jwt_data.get("role")

    if role != "admin":
        return jsonify({"error": "Access denied"}), 403  # Forbidden

    return jsonify({"message": f"Welcome Admin, you have full access!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

