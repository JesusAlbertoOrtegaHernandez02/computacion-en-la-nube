from flask import Flask, request
from flask_cors import CORS
from crud import create_item, get_item, get_items, update_item, delete_item

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/items', methods=['POST'])
def create(): return create_item(request.json)

@app.route('/items', methods=['GET'])
def get_all(): return get_items()

@app.route('/items/<string:item_id>', methods=['GET'])
def get_one(item_id): return get_item(item_id)

@app.route('/items/<string:item_id>', methods=['PUT'])
def update(item_id): return update_item(item_id, request.json)

@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete(item_id): return delete_item(item_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
