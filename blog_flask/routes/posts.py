from flask import Blueprint, request, jsonify
from models.db import posts
from bson import ObjectId
from datetime import datetime

posts_bp = Blueprint("posts", __name__)

@posts_bp.post("/posts")
def create_post():
    data = request.json

    post = {
        "title": data.get("title"),
        "content": data.get("content"),
        "author_id": ObjectId(data.get("author_id")),
        "tags": data.get("tags", []),
        "created_at": datetime.utcnow(),
        "likes": 0
    }

    posts.insert_one(post)

    return jsonify({"message": "Post created"}), 201


@posts_bp.get("/posts")
def get_all_posts():
    response = []
    for p in posts.find():
        p["_id"] = str(p["_id"])
        p["author_id"] = str(p["author_id"])
        response.append(p)
    return jsonify(response)


@posts_bp.get("/posts/<id>")
def get_post(id):
    post = posts.find_one({"_id": ObjectId(id)})
    if not post:
        return jsonify({"error": "Not found"}), 404

    post["_id"] = str(post["_id"])
    post["author_id"] = str(post["author_id"])
    return jsonify(post)


@posts_bp.delete("/posts/<id>")
def delete_post(id):
    posts.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted"})
