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

# In-memory order storage
orders = []
next_order_id = 1

@app.route('/order', methods=['POST'])
def create_order():
    global next_order_id
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    # Simple validation
    if not user_id or not product_id:
        return jsonify({'message': 'User ID and Product ID are required'}), 400

    # Create order
    order = {'id': next_order_id, 'user_id': user_id, 'product_id': product_id, 'status': 'Pending'}
    orders.append(order)
    next_order_id += 1
    return jsonify({'message': 'Order created successfully', 'order': order}), 201

@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            return jsonify({'order': order}), 200

    return jsonify({'message': 'Order not found'}), 404

@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify({'orders': orders}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
