from models.models import Status, StatusQuery
from uagents import Context
from uagents.protocol import Protocol

delivery_protocol = Protocol(name="delivery-protocol", version="1.0.0")


@delivery_protocol.on_message(model=StatusQuery, replies=Status)
async def query_handler(ctx: Context, sender: str, _: StatusQuery):
    if not ctx.storage.has("status"):
        ctx.storage.set("name", ctx.name)
        ctx.storage.set("status", "IDLE")
        ctx.storage.set("order", "")
        ctx.storage.set("in_store", False)
    await ctx.send(
        sender,
        Status(
            name=ctx.storage.get("name"),
            status=ctx.storage.get("status"),
            in_store=ctx.storage.get("in_store"),
            order=ctx.storage.get("order"),
        ),
    )
