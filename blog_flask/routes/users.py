from flask import Blueprint, request, jsonify
import bcrypt
from models.db import users
from bson import ObjectId

users_bp = Blueprint("users", __name__)

@users_bp.post("/register")
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return jsonify({"error": "Email exists"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = {
        "username": username,
        "email": email,
        "password_hash": hashed.decode(),
        "role": "author",
        "status": "active"
    }

    users.insert_one(user)
    return jsonify({"message": "User registered"}), 201


@users_bp.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"error": "Wrong password"}), 400

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
    })
