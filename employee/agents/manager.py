from models.models import Status, Statuses, StatusQuery, GetStatus
from uagents import Agent, Context

from protocols.delivery_protocol import delivery_protocol

manager = Agent(
    name="manager",
    seed="manager-seed-phrase",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

print("Manager: ", manager.address)

addresses = [
    "agent1qfhgl8s04lkaf44xgc5ch2jlhz9kpcd7wppfedjvfayqwhde2jh8g52zy8d",
    "agent1q26w5lt5rn6kw8kdut9c4pvf5cxuam3py5dk72s9hasfwkftuc9277c8pda",
]


@manager.on_interval(period=5)
async def query_handler(ctx: Context):
    print("Status requested")
    await ctx.experimental_broadcast(
        destination_protocol=delivery_protocol.digest, message=StatusQuery()
    )


@manager.on_message(model=Status)
async def status_handler(ctx: Context, sender: str, status: Status):
    print("Status received", sender, status)
    ctx.storage.set(sender, status.dict())


@manager.on_message(model=GetStatus, replies=Statuses)
async def get_status_handler(ctx: Context, sender: str, _: GetStatus):
    statuses = []
    for address in addresses:
        status = ctx.storage.get(address)
        statuses.append(Status(**status))

    await ctx.send(sender, Statuses(statuses=statuses))
