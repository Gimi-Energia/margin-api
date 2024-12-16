import uuid
from typing import Optional

from ninja import Schema


class CompanyCreateSchema(Schema):
    name: str
    profit_type: str


class CompanySchema(CompanyCreateSchema):
    id: uuid.UUID


class CompanyListSchema(Schema):
    count: int
    companies: list[CompanySchema]


class CompanyUpdateSchema(Schema):
    name: Optional[str] = None
    profit_type: Optional[str] = None


class PercentageSchema(Schema):
    id: uuid.UUID
    value: float


class PercentageListSchema(Schema):
    count: int
    percentages: list[PercentageSchema]


class PercentageUpdateSchema(Schema):
    value: Optional[float] = None


class ProductSchema(Schema):
    index: int
    name: str
    ncm: str
    current_value: float
    contribution_percentage: float


class ContractSchema(Schema):
    # id: uuid.UUID
    contract_id: int
    contract_number: str
    company: int
    client_name: str
    client_id: int
    construction_name: str
    current_sale_value: float
    cost_value: float
    freight_value: float
    commission: float
    state: str
    icms: float
    other_taxes: float
    account: int
    installments: int
    xped: str | None = None
    items: list[ProductSchema]
