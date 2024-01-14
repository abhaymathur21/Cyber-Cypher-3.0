import json

from agents.manager import manager
from flask import Flask, render_template, request
from flask_cors import CORS
from models.models import GetStatus, GetOrders
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
