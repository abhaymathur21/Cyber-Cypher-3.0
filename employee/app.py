from flask import Flask, request, render_template
from uagents.query import query
from flask_cors import CORS
import json

from agents.manager import manager


from models.models import GetStatus

app = Flask(__name__)
CORS(app)

destination = manager.address


@app.get("/")
def index():
    return render_template("index.html", message="")


@app.post("/")
async def form():
    data = request.form["data"]
    res = await query(destination=destination, message=GetStatus())
    print(res.decode_payload())
    statuses = json.loads(res.decode_payload())["statuses"]
    print(statuses)

    return render_template("index.html", statuses=statuses)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
