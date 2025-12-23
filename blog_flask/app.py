from flask import Flask, jsonify
from routes.users import users_bp
from routes.posts import posts_bp

app = Flask(__name__)

app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)

@app.get("/")
def home():
    return jsonify({"message": "Blog API running!"})

if __name__ == "__main__":
    app.run(debug=True)
