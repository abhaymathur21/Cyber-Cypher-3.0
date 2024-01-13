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


@manager.on_interval(period=10)
async def update_status(ctx: Context):
    print("-" * 20)
    ctx.logger.info("Status requested", delivery_protocol.digest)
    await ctx.experimental_broadcast(
        destination_protocol=delivery_protocol.digest, message=StatusQuery()
    )


@manager.on_message(model=Status)
async def status_handler(ctx: Context, sender: str, status: Status):
    ctx.logger.info("Status received", sender, status)
    ctx.storage.set(sender, status.dict())


@manager.on_query(model=GetStatus, replies=Statuses)
async def get_status_handler(ctx: Context, sender: str, _: GetStatus):
    statuses = []
    for address in ctx.storage._data.keys():
        status = ctx.storage.get(address)
        statuses.append(Status(**status))

    await ctx.send(sender, Statuses(statuses=statuses))
