"""
This module starts the API server and defines the family endpoints.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family before defining the routes
jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def sitemap():
    return generate_sitemap(app)


# 1. Get all family members
@app.route("/members", methods=["GET"])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


# 2. Get one family member
@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = jackson_family.get_member(member_id)

    if member is None:
        return jsonify({"error": "Family member not found"}), 404

    return jsonify(member), 200


# 3. Add a new family member
@app.route("/members", methods=["POST"])
def add_member():
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["first_name", "age", "lucky_numbers"]

    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if not isinstance(body["first_name"], str) or not body["first_name"].strip():
        return jsonify({"error": "first_name must be a non-empty string"}), 400

    if (
        not isinstance(body["age"], int)
        or isinstance(body["age"], bool)
        or body["age"] <= 0
    ):
        return jsonify({"error": "age must be an integer greater than 0"}), 400

    if (
        not isinstance(body["lucky_numbers"], list)
        or not all(
            isinstance(number, int) and not isinstance(number, bool)
            for number in body["lucky_numbers"]
        )
    ):
        return jsonify({"error": "lucky_numbers must be a list of integers"}), 400

    new_member = jackson_family.add_member(body)
    return jsonify(new_member), 200


# 4. Delete one family member
@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)

    if not deleted:
        return jsonify({"error": "Family member not found"}), 404

    return jsonify({"done": True}), 200


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)