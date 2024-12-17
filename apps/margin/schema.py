import uuid
from typing import Optional

from ninja import Schema
from apps.icms.schema import (
    ICMSRateContractSchema,
    StateContractSchema,
    NCMContractSchema,
)


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


class CompanyContractSchema(Schema):
    name: str


class PercentageContractSchema(Schema):
    value: float


class ProductSchema(Schema):
    # id: uuid.UUID
    index: int
    name: str
    contribution_rate: float
    # sale_item_id: int
    # quantity: int
    # product_id: int
    # updated_value: float


class ContractSchema(Schema):
    # id: uuid.UUID
    # contract_id: int
    contract_number: str
    company: CompanyContractSchema
    client_name: str
    # client_id: int
    construction_name: str
    net_cost: float
    net_cost_without_taxes: float
    # net_cost_with_margin: float
    freight_value: float
    commission: float
    state: StateContractSchema
    ncm: NCMContractSchema
    icms: ICMSRateContractSchema
    other_taxes: float
    # account: int
    # installments: int
    # xped: str
    # margin: PercentageContractSchema
    items: list[ProductSchema]
