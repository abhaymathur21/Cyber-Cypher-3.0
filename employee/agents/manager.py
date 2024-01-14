from models.models import (
    Status,
    Statuses,
    StatusQuery,
    GetStatus,
    CreateOrder,
    Success,
    Order,
    OrderID,
    GetOrders,
    Orders,
)
from uagents import Agent, Context

from protocols.delivery_protocol import delivery_protocol

manager = Agent(
    name="manager",
    seed="manager-seed-phrase",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

print("Manager: ", manager.address)


@manager.on_event("startup")
async def startup_handler(ctx: Context):
    if not ctx.storage.has("orders"):
        ctx.storage.set("orders", [])

    if not ctx.storage.has("statuses"):
        ctx.storage.set("statuses", [])

    if not ctx.storage.has("order_id"):
        ctx.storage.set("order_id", 0)

    if not ctx.storage.has("last_assigned"):
        ctx.storage.set("last_assigned", "")

    ctx.logger.info("Manager started")


@manager.on_interval(period=10)
async def update_status(ctx: Context):
    print("-" * 20)
    ctx.logger.info(f"Status requested: {delivery_protocol.digest}")
    await ctx.experimental_broadcast(
        destination_protocol=delivery_protocol.digest, message=StatusQuery()
    )


@manager.on_message(model=Status)
async def status_handler(ctx: Context, sender: str, status: Status):
    ctx.logger.info(f"Status received: {status.json()}")

    statuses = ctx.storage.get("statuses")
    statuses = list(filter(lambda s: s["address"] != sender, statuses))
    statuses.append(status.dict())
    ctx.storage.set("statuses", statuses)


@manager.on_query(model=GetStatus, replies=Statuses)
async def get_status_handler(ctx: Context, sender: str, _: GetStatus):
    statuses = [Status(**status) for status in ctx.storage.get("statuses")]
    await ctx.send(sender, Statuses(statuses=statuses))


@manager.on_query(model=CreateOrder, replies=Success)
async def create_order_handler(ctx: Context, sender: str, orderQuery: CreateOrder):
    next_id = ctx.storage.get("order_id")

    order = {
        **orderQuery.dict(),
        "status": "PENDING",
        "id": next_id,
        "delivery_agent": "",
    }

    ctx.storage.set("order_id", next_id + 1)

    orders = ctx.storage.get("orders")
    orders.append(order)
    ctx.storage.set("orders", orders)

    await ctx.send(sender, Success(success=True))


@manager.on_interval(period=10)
async def assign_order(ctx: Context):
    orders = ctx.storage.get("orders")
    statuses = ctx.storage.get("statuses")

    last_assigned = ctx.storage.get("last_assigned")

    for status in statuses:
        if (
            status["status"] == "IDLE"
            and status["in_store"]
            and status["address"] != last_assigned
        ):
            if len(orders) > 0:
                pending_orders = list(
                    filter(lambda order: order["status"] == "PENDING", orders)
                )
                if len(pending_orders) == 0:
                    break

                order = pending_orders[0]

                for o in orders:
                    if o["id"] == order["id"]:
                        o["status"] = "ASSIGNED"
                        o["delivery_agent"] = status["name"]
                        break

                ctx.storage.set("orders", orders)

                ctx.storage.set("last_assigned", status["address"])

                await ctx.send(
                    status["address"], OrderID(id=order["id"], status="ASSIGNED")
                )
                break


@manager.on_message(model=OrderID)
async def order_id_handler(ctx: Context, sender: str, order_id: OrderID):
    orders = ctx.storage.get("orders")

    for order in orders:
        if order["id"] == order_id.id:
            order["status"] = order_id.status
            ctx.storage.set("orders", orders)
            break

    if order_id.status == "DELIVERING":
        await ctx.send(
            sender,
            OrderID(
                id=order_id.id,
                status="DELIVERING",
            ),
        )


@manager.on_query(model=GetOrders, replies=Orders)
async def get_orders_handler(ctx: Context, sender: str, _: GetOrders):
    orders = [Order(**order) for order in ctx.storage.get("orders")]
    await ctx.send(sender, Orders(orders=orders))


@manager.on_event("shutdown")
async def shutdown_handler(ctx: Context):
    ctx.logger.info("Shutting down")
    ctx.storage.set("statuses", [])
    await ctx.stop()
