import uuid

from ninja import Schema


class StateSchema(Schema):
    id: uuid.UUID
    name: str
    code: str


class NCMSUpdateSchema(Schema):
    code: str | None = None
    group: uuid.UUID | None = None


class NCMSCreateSchema(Schema):
    code: str
    group: uuid.UUID


class NCMSchema(Schema):
    id: uuid.UUID
    code: str


class NCMGroupCreateSchema(Schema):
    name: str


class NCMGroupRateSchema(NCMGroupCreateSchema):
    id: uuid.UUID


class NCMGroupSchema(NCMGroupCreateSchema):
    id: uuid.UUID
    ncms: list[NCMSchema]


class ICMSRateCreateSchema(Schema):
    state: uuid.UUID
    group: uuid.UUID
    internal_rate: float
    difal_rate: float
    poverty_rate: float


class ICMSRateUpdateSchema(Schema):
    state: uuid.UUID | None = None
    group: uuid.UUID | None = None
    internal_rate: float | None = None
    difal_rate: float | None = None
    poverty_rate: float | None = None


class ICMSRateSchema(Schema):
    id: uuid.UUID
    state: StateSchema
    group: NCMGroupRateSchema
    internal_rate: float
    difal_rate: float
    poverty_rate: float
    total_rate: float
