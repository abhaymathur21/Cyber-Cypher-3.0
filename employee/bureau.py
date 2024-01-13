from agents.manager import manager
from protocols.delivery_protocol import delivery_protocol
from uagents import Agent, Bureau
from uagents.setup import fund_agent_if_low

bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)


for i in range(3):
    delivery = Agent(
        name=f"delivery agent {chr(i+65)}",
        seed=f"delivery-seed-phrase-{i}",
        port=8001 + i,
        endpoint=[f"http://127.0.0.1:800{i+1}/submit"],
    )

    delivery.include(delivery_protocol, True)
    fund_agent_if_low(delivery.wallet.address())

    print(delivery.name, delivery.address)

    bureau.add(delivery)

bureau.add(manager)

if __name__ == "__main__":
    bureau.run()
