import uuid

from ninja import Schema


class TaxCreateSchema(Schema):
    name: str
    presumed_profit_rate: float
    real_profit_rate: float


class TaxSchema(TaxCreateSchema):
    id: uuid.UUID


class TaxListSchema(Schema):
    total: int
    taxes: list[TaxSchema]


class TaxUpdateSchema(Schema):
    name: str | None = None
    presumed_profit_rate: float | None = None
    real_profit_rate: float | None = None
