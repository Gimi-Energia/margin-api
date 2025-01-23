import uuid
from typing import Optional

from ninja import Schema


class TaxCreateSchema(Schema):
    name: str
    presumed_profit_rate: float
    real_profit_rate: float


class TaxSchema(TaxCreateSchema):
    id: uuid.UUID


class TaxListSchema(Schema):
    count: int
    total_presumed_profit_rate: float
    total_real_profit_rate: float
    taxes: list[TaxSchema]


class TaxUpdateSchema(Schema):
    name: Optional[str] = None
    presumed_profit_rate: Optional[float] = None
    real_profit_rate: Optional[float] = None


class TaxByCompanySchema(Schema):
    id: uuid.UUID
    name: str
    rate: float
