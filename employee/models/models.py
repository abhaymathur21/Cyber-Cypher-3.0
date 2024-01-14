from uagents import Model


class StatusQuery(Model):
    pass


class Status(Model):
    name: str
    address: str
    status: str
    in_store: bool
    order: str


class Statuses(Model):
    statuses: list[Status]


class Success(Model):
    success: bool


class GetStatus(Model):
    pass


class CreateOrder(Model):
    product_id: int
    quantity: int
    customer_id: str


class Order(Model):
    id: int
    product_id: int
    quantity: int
    customer_id: str
    status: str
    delivery_agent: str


class OrderID(Model):
    id: int
    status: str


class GetOrders(Model):
    pass


class Orders(Model):
    orders: list[Order]
