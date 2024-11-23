from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)


# Database connection
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = os.environ.get('MYSQL_PORT')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')

connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

# In-memory product storage
products = []
next_product_id = 1

@app.route('/add', methods=['POST'])
def add_product():
    global next_product_id
    data = request.get_json()
    name = data.get('name')

    # Simple validation
    if not name:
        return jsonify({'message': 'Product name is required'}), 400

    # Add product
    product = {'id': next_product_id, 'name': name}
    products.append(product)
    next_product_id += 1
    return jsonify({'message': 'Product added successfully', 'product': product}), 201

@app.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            return jsonify({'message': 'Product deleted successfully'}), 200

    return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify({'products': products}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
