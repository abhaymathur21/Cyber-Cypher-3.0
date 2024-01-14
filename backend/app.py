from flask import Flask, request, render_template, jsonify
from uagents.query import query
from uagents import Model
from flask_cors import CORS
import json
from collections import OrderedDict

class Message(Model):
    product: str
    quantity: str
    

app = Flask(__name__)
CORS(app)

json_file_path = r'C:\Users\a21ma\OneDrive\Desktop\Cyber Cypher 3.0\data\products.json'

# Reading the data from the json file:
with open(json_file_path, 'r') as json_file:
    products_data = json.load(json_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
async def frontend_input():
    if request.method== 'POST':
        data = request.json
        product = data.get('product')
        quantity = data.get('quantity')
        await query(destination='agent1qgmvuf8wuv96ypmsptary360n8qghm80yw0tv39qqk4d5nepgudxzskzqqm',message=Message(product=product,quantity=quantity)) # goes to input agent
        processed_result = f"You have successfully bought: {product} and the quantity is {quantity}"
        return processed_result
    return processed_result   

@app.route('/product-suggestions', methods=['GET'])
def product_suggestions():
    input_text = request.args.get('input', '')

    # Filter suggestions based on the input_text from the loaded products data
    # print(product['name'] for product in products_data)
    filtered_suggestions = [
        {"Name": product['Name'], "Size": product['Size']}
        for product in products_data
        if isinstance(product, dict) and 'Name' in product and 'Size' in product and product['Name'].lower().startswith(input_text.lower())
    ]
    return jsonify(filtered_suggestions)

@app.route('/products', methods=['GET','POST'])
def products():
    if request.method == 'GET':

        return jsonify(products_data)
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Updating the json file:
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        
        # print(product, quantity)
        return jsonify({"message": "Data updated successfully"})
        
if __name__ == '__main__':
    app.run(debug=True)
