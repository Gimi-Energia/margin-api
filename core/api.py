from ninja import NinjaAPI, Redoc

from apps.icms.api import icms_router, ncm_router, state_router
from apps.margin.api import company_router, percentage_router, contract_router
from apps.taxes.api import taxes_router

api = NinjaAPI(
    csrf=False,
    title="Margin API",
    version="1.0.0",
    description="This is a API to manage profit margin data",
)

api.add_router("/icms", icms_router, tags=["ICMS"])
api.add_router("/ncm", ncm_router, tags=["NCM"])
api.add_router("/states", state_router, tags=["States"])
api.add_router("/taxes", taxes_router, tags=["Taxes"])
api.add_router("/companies", company_router, tags=["Companies"])
api.add_router("/percentages", percentage_router, tags=["Percentages"])
api.add_router("/contracts", contract_router, tags=["Contracts"])
