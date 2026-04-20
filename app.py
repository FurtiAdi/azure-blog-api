from flask import Flask, jsonify, request
import uuid
from datetime import datetime
from services.cosmos_service import container

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Blog API is running!"})


# POST
@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    if not data or not all(k in data for k in ("title", "content", "author")):
        return jsonify({"error": "Missing required fields"}), 400

    post = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "timestamp": datetime.utcnow().isoformat()
    }

    container.create_item(body=post)

    return jsonify(post), 201


# GET ALL
@app.route("/posts", methods=["GET"])
def get_posts():
    query = "SELECT * FROM c"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    return jsonify(items), 200


# GET BY ID
@app.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    query = "SELECT * FROM c WHERE c.id = @id"
    parameters = [{"name": "@id", "value": post_id}]

    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if not items:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(items[0]), 200


if __name__ == "__main__":
    app.run(debug=True)