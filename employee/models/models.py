from uagents import Model


class StatusQuery(Model):
    pass


class Status(Model):
    status: str
    in_store: bool
    order: str


class Statuses(Model):
    statuses: list[Status]


class Success(Model):
    success: bool


class GetStatus(Model):
    pass
