from protocols.delivery_protocol import delivery_protocol
from uagents import Agent

delivery = Agent(
    name="delivery",
    seed="delivery-seed-phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

print("Delivery: ", delivery.address)


delivery.include(delivery_protocol)
