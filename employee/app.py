import json

from agents.manager import manager
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
from models.models import GetStatus, GetOrders, CreateOrder
from uagents.query import query

app = Flask(__name__)
CORS(app)

destination = manager.address


@app.get("/")
async def index():
    res = await query(destination=destination, message=GetStatus())
    statuses = json.loads(res.decode_payload())["statuses"] if res else []

    res = await query(destination=destination, message=GetOrders())
    orders = json.loads(res.decode_payload())["orders"] if res else []

    print(statuses, orders)

    return render_template("index.html", statuses=statuses, orders=orders)


@app.get("/orders")
async def orders():
    res = await query(destination=destination, message=GetOrders())
    orders = json.loads(res.decode_payload())["orders"] if res else []

    with open("../data/products.json", "r") as f:
        products = json.load(f)

    return render_template("orders.html", orders=orders, products=products)


@app.post("/create-order")
async def create_order():
    customer_id = request.form["customer_id"]
    product = request.form["product"]
    quantity = request.form["quantity"]

    res = await query(
        destination=destination,
        message=CreateOrder(
            product_id=product, quatity=quantity, customer_id=customer_id
        ),
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
