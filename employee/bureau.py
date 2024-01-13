from uagents import Bureau
from agents.manager import manager
from agents.delivery import delivery

bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)

bureau.add(manager)
bureau.add(delivery)

if __name__ == "__main__":
    bureau.run()
