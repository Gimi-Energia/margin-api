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


class ProductFindSchema(Schema):
    id: uuid.UUID
    index: int
    name: str
    contribution_rate: float


class ProductCalculateSchema(ProductFindSchema):
    updated_value: float


class ContractFindSchema(Schema):
    id: uuid.UUID
    contract_number: str
    company: CompanyContractSchema
    client_name: str
    construction_name: str
    net_cost: float
    net_cost_without_taxes: float
    freight_value: float
    commission: float
    state: StateContractSchema
    ncm: NCMContractSchema
    icms: ICMSRateContractSchema
    other_taxes: float
    is_end_consumer: bool
    end_consumer_rate: float
    is_icms_taxpayer: bool
    taxes_considered: str
    items: list[ProductFindSchema]


class ContractCalculateSchema(Schema):
    id: uuid.UUID
    contract_number: str
    company: CompanyContractSchema
    client_name: str
    construction_name: str
    net_cost: float
    net_cost_without_taxes: float
    net_cost_with_margin: float
    freight_value: float
    commission: float
    state: StateContractSchema
    ncm: NCMContractSchema
    icms: ICMSRateContractSchema
    other_taxes: float
    margin: PercentageContractSchema
    is_end_consumer: bool
    end_consumer_rate: float
    admin_rate: float
    taxes_considered: str
    is_icms_taxpayer: bool
    items: list[ProductCalculateSchema]


class ContractReturnSchema(Schema):
    detail: str
    url: str
