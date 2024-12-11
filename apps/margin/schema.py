import uuid

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
    name: str | None = None
    profit_type: str | None = None


class PercentageSchema(Schema):
    id: uuid.UUID
    value: float


class PercentageListSchema(Schema):
    count: int
    percentages: list[PercentageSchema]


class PercentageUpdateSchema(Schema):
    value: float | None = None
