from uagents.setup import fund_agent_if_low
from uagents import Agent, Context

from models.models import StatusQuery, Status

manager = Agent(
    name="manager",
    port=8000,
    seed="manager-seed-phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(manager.wallet.address())

print("Manager: ", manager.address)


@manager.on_query(model=StatusQuery, replies=Status)
async def query_handler(ctx: Context, sender: str, _: StatusQuery):
    print("Status requested")
    await ctx.send(sender, Status(message="Hello"))
