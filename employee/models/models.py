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


class Product(Model):
    id: int
    quatity: int


class CreateOrder(Model):
    products: list[Product]
    customer_id: str


class Order(Model):
    id: int
    products: str
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
