from flask import Flask, request, render_template
from uagents.query import query
from uagents import Model
from flask_cors import CORS

class Message(Model):
    product: str
    quantity: str
    

app = Flask(__name__)
CORS(app)

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
        
if __name__ == '__main__':
    app.run(debug=True)
