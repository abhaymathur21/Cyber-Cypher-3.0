from random import randint
from time import sleep

from models.models import OrderID, Status, StatusQuery
from uagents import Context
from uagents.protocol import Protocol

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
    ctx.logger.info(f"Order received: {order_id.id} {order_id.status}")

    if order_id.status == "ASSIGNED":
        ctx.storage.set("order", order_id.id)
        ctx.storage.set("status", "DELIVERING")
        ctx.storage.set("in_store", False)

        sleep(randint(3, 5))

        ctx.logger.info(f"Order assigned: {order_id.id}")

        await ctx.send(sender, OrderID(id=order_id.id, status="DELIVERING"))

    elif order_id.status == "DELIVERING":
        ctx.storage.set("status", "IDLE")
        ctx.storage.set("in_store", True)
        ctx.storage.set("order", "")

        sleep(randint(5, 10))

        ctx.logger.info(f"Order delivered: {order_id.id}")

        await ctx.send(sender, OrderID(id=order_id.id, status="DELIVERED"))

    else:
        ctx.logger.info("Order not found", order_id.id)
        await ctx.send(sender, OrderID(id=order_id.id, status="NOT FOUND"))
