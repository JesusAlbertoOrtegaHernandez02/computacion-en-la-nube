from flask import jsonify
from db.dynamodb_db import DynamoDB

db = DynamoDB()

def create_item(data):
    if "id" not in data:
        return jsonify({"error": "Falta el campo 'id'"}), 400
    result = db.create_item(data)
    return jsonify(result), 201

def get_item(item_id):
    result = db.get_item(item_id)
    if not result:
        return jsonify({"error": "Elemento no encontrado"}), 404
    return jsonify(result), 200

def get_items():
    result = db.get_all_items()
    return jsonify(result), 200

def update_item(item_id, data):
    result = db.update_item(item_id, data)
    return jsonify(result), 200

def delete_item(item_id):
    result = db.delete_item(item_id)
    return jsonify(result), 200
