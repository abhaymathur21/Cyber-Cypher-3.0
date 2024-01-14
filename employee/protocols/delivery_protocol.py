from models.models import Status, StatusQuery, OrderID
from uagents import Context
from uagents.protocol import Protocol

from time import sleep

delivery_protocol = Protocol(name="delivery-protocol", version="1.0.0")


@delivery_protocol.on_message(model=StatusQuery, replies=Status)
async def query_handler(ctx: Context, sender: str, _: StatusQuery):
    if not ctx.storage.has("status"):
        ctx.storage.set("name", ctx.name)
        ctx.storage.set("address", ctx.address)
        ctx.storage.set("status", "IDLE")
        ctx.storage.set("order", "")
        ctx.storage.set("in_store", True)
    await ctx.send(
        sender,
        Status(
            name=ctx.storage.get("name"),
            address=ctx.storage.get("address"),
            status=ctx.storage.get("status"),
            in_store=ctx.storage.get("in_store"),
            order=ctx.storage.get("order"),
        ),
    )


@delivery_protocol.on_message(model=OrderID, replies=OrderID)
async def order_id_handler(ctx: Context, sender: str, order_id: OrderID):
    if order_id.status == "ASSIGNED":
        ctx.storage.set("order", order_id.id)
        ctx.storage.set("status", "DELIVERING")
        ctx.storage.set("in_store", False)

        ctx.logger.info(f"Order received: {order_id.id}")

        sleep(10)

        await ctx.send(sender, OrderID(id=order_id.id, status="DElIVERING"))

    elif order_id.status == "DELIVERING":
        ctx.storage.set("status", "IDLE")
        ctx.storage.set("in_store", True)
        ctx.storage.set("order", "")

        ctx.logger.info(f"Order delivered: {order_id.id}")

        sleep(10)

        await ctx.send(sender, OrderID(id=order_id.id))

    else:
        ctx.logger.info("Order not found", order_id.id)
        await ctx.send(sender, OrderID(id=order_id.id, status="NOT FOUND"))
