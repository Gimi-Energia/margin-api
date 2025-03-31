import uuid
from typing import Optional

from ninja import Schema


class StateSchema(Schema):
    id: uuid.UUID
    name: str
    code: str


class StateListSchema(Schema):
    count: int
    states: list[StateSchema]


class NCMSUpdateSchema(Schema):
    code: Optional[str] = None
    percentage_end_consumer: Optional[float] = None
    group: Optional[uuid.UUID] = None


class NCMSCreateSchema(Schema):
    code: str
    percentage_end_consumer: float
    group: uuid.UUID


class NCMGroupCreateSchema(Schema):
    name: str


class NCMGroupRateSchema(NCMGroupCreateSchema):
    id: uuid.UUID


class NCMSchema(Schema):
    id: uuid.UUID
    code: str
    percentage_end_consumer: float


class NCMSchemaWithGroup(NCMSchema):
    group: NCMGroupRateSchema


class NCMSListchema(Schema):
    count: int
    ncms: list[NCMSchemaWithGroup]


class NCMGroupSchema(NCMGroupCreateSchema):
    id: uuid.UUID
    ncms: list[NCMSchema]


class NCMGroupListSchema(Schema):
    count: int
    ncm_groups: list[NCMGroupSchema]


class ICMSRateCreateSchema(Schema):
    state: uuid.UUID
    group: uuid.UUID
    internal_rate: float
    difal_rate: float
    poverty_rate: float


class ICMSRateBulkCreateSchema(Schema):
    rates: list[ICMSRateCreateSchema]


class ICMSRateUpdateSchema(Schema):
    state: Optional[uuid.UUID] = None
    group: Optional[uuid.UUID] = None
    internal_rate: Optional[float] = None
    difal_rate: Optional[float] = None
    poverty_rate: Optional[float] = None


class ICMSRateBulkUpdateSchema(Schema):
    rates: list[ICMSRateUpdateSchema]


class ICMSRateSchema(Schema):
    id: uuid.UUID
    state: StateSchema
    group: NCMGroupRateSchema
    internal_rate: float
    difal_rate: float
    poverty_rate: float
    total_rate: float


class ICMSRateListSchema(Schema):
    count: int
    icms_rates: list[ICMSRateSchema]


class ICMSRateContractSchema(Schema):
    total_rate: float


class StateContractSchema(Schema):
    name: str
    code: str


class NCMContractSchema(Schema):
    code: str
    percentage_end_consumer: float
