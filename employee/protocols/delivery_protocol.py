from uagents import Protocol, Context

from models.models import StatusQuery, Status, Statuses

delivery_protocol = Protocol(name="delivery-protocol")


@delivery_protocol.on_message(model=StatusQuery, replies=Status)
async def query_handler(ctx: Context, sender: str, _: StatusQuery):
    if not ctx.storage.has("status"):
        ctx.storage.set("status", "IDLE")
        ctx.storage.set("order", "")
        ctx.storage.set("in_store", False)

    print("Status requested", sender)
    await ctx.send(
        sender,
        Status(
            status=ctx.storage.get("status"),
            in_store=ctx.storage.get("in_store"),
            order=ctx.storage.get("order"),
        ),
    )
