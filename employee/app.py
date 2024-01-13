from flask import Flask, request, render_template
from uagents.query import query
from flask_cors import CORS
import json

from agents.manager import manager


from models.models import StatusQuery

app = Flask(__name__)
CORS(app)

# destination = "agent1q22hcm833jf2atptpjmepvpaftwzg0kvh4ztp9xlulf6w40utvrqjcnr6hu"
destination = manager.address


@app.get("/")
def index():
    return render_template("index.html", message="")


@app.post("/")
async def form():
    data = request.form["data"]
    res = await query(destination=destination, message=StatusQuery())
    res_data = json.loads(res.decode_payload()) if res else {"message": "No response"}

    return render_template("index.html", message=f"Recieved: {res_data['message']}")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
